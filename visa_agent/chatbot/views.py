from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import VisaSearch
from .serializers import VisaSearchSerializer
from .visa_manager import VisaManager
from django.http import JsonResponse
from rest_framework.decorators import action

class VisaSearchViewSet(viewsets.ModelViewSet):
    queryset = VisaSearch.objects.all()
    serializer_class = VisaSearchSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Create VisaSearch instance but don't save yet
            visa_search = serializer.save(status='processing')
            
            try:
                # Initialize VisaManager and get results
                visa_manager = VisaManager(
                    country=visa_search.country,
                    visa_type=visa_search.visa_type
                )
                result = visa_manager.run()
                
                # Update the instance with results
                if result.get("status") == "success":
                    visa_search.status = "success"
                    visa_search.embassy_url = result.get("embassy_url")
                    visa_search.visa_information = result.get("visa_information")
                else:
                    visa_search.status = "error"
                    visa_search.visa_information = result.get("message")
                
                visa_search.save()
                return Response(
                    self.get_serializer(visa_search).data,
                    status=status.HTTP_201_CREATED
                )
            
            except Exception as e:
                visa_search.status = "error"
                visa_search.visa_information = str(e)
                visa_search.save()
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=['get'])
    def search(self, request):
        country = request.query_params.get('country')
        visa_type = request.query_params.get('visa_type')
        
        if not country or not visa_type:
            return Response(
                {"error": "Both country and visa_type parameters are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Check if we have cached results
        recent_search = VisaSearch.objects.filter(
            country=country,
            visa_type=visa_type,
            status='success'
        ).first()
        
        if recent_search:
            serializer = self.get_serializer(recent_search)
            return Response(serializer.data)
            
        # If no cached results, create new search
        return self.create(request)
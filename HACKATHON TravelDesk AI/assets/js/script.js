
// // Show and hide chatbot window
// document.getElementById('chatbot-button').onclick = function () {
//     document.getElementById('chatbot-window').style.display = 'flex';
//     document.getElementById('chatbot-button').style.display = 'none';
// };

// // Close the chatbot window
// function closeChatbot() {
//     document.getElementById('chatbot-window').style.display = 'none';
//     document.getElementById('chatbot-button').style.display = 'flex';
// }

// // Send a message when user presses "Send" button
// function sendMessage() {
//     let userInput = document.getElementById('user-input').value;
//     if (userInput.trim() !== "") {
//         // Display user message
//         displayMessage(userInput, "user");

//         // Process and display bot response
//         processBotResponse(userInput);
//         document.getElementById('user-input').value = ""; // Clear input field
//     }
// }

// // Display messages in the chatbot
// function displayMessage(message, sender) {
//     const chatbotContent = document.getElementById('chatbot-content');
//     const messageDiv = document.createElement('div');
//     messageDiv.classList.add('message', sender + '-message');
//     messageDiv.innerHTML = `<p>${message}</p>`;
//     chatbotContent.appendChild(messageDiv);
//     chatbotContent.scrollTop = chatbotContent.scrollHeight; // Scroll to the latest message
// }

// // Process the user's input and generate bot responses
// function processBotResponse(userInput) {
//     const chatbotContent = document.getElementById('chatbot-content');
//     let responseMessage = "";

//     if (userInput.toLowerCase().includes("visa status")) {
//         responseMessage = "Please provide your application reference number and date of birth to check the status.";
//     } else if (userInput.toLowerCase().includes("check visa status")) {
//         responseMessage = "I’m checking your visa status now...";
//     } else if (userInput.toLowerCase().includes("document checklist")) {
//         responseMessage = "Here’s a general checklist for visa applications: Passport, Application form, Passport photos, etc.";
//     } else if (userInput.toLowerCase().includes("help") || userInput.toLowerCase().includes("assistant")) {
//         responseMessage = "How can I assist you today? Choose an option like 'Visa Status' or 'Document Checklist'.";
//     } else {
//         responseMessage = "Sorry, I didn't quite understand. Could you ask something else?";
//     }

//     displayMessage(responseMessage, "bot");
// }


// Show and hide chatbot window based on service button clicked

// document.getElementById('chatbot-button').onclick = function () {
//     document.getElementById('chatbot-window').style.display = 'flex';
//     document.getElementById('chatbot-button').style.display = 'none';
// };


document.getElementById('mock-chatbot-button').onclick = function () {
    openChatbot('mock-chatbot-content');
};

document.getElementById('visa-requirements-chatbot-button').onclick = function () {
    openChatbot('visa-requirements-content');
};

document.getElementById('visa-guidance-chatbot-button').onclick = function () {
    openChatbot('visa-guidance-content');
};

document.getElementById('document-auth-chatbot-button').onclick = function () {
    openChatbot('document-auth-content');
};

// Open the chatbot window with specific content based on the service clicked
function openChatbot(contentId) {
    document.getElementById('chatbot-window').style.display = 'flex';
    document.getElementById('chatbot-button').style.display = 'none';

    // Hide all content sections and show the selected one
    const contentSections = document.querySelectorAll('.chatbot-content');
    contentSections.forEach(section => section.style.display = 'none');
    document.getElementById(contentId).style.display = 'block';
}

// Close the chatbot window
function closeChatbot() {
    document.getElementById('chatbot-window').style.display = 'none';
    document.getElementById('chatbot-button').style.display = 'flex';
}

// Send a message when user presses "Send" button
function sendMessage() {
    let userInput = document.getElementById('user-input').value;
    if (userInput.trim() !== "") {
        displayMessage(userInput, "user");
        processBotResponse(userInput);
        document.getElementById('user-input').value = ""; // Clear input field
    }
}

// Display messages in the chatbot
function displayMessage(message, sender) {
    const chatbotContent = document.querySelector('.chatbot-content[style="display: block;"]');
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', sender + '-message');
    messageDiv.innerHTML = `<p>${message}</p>`;
    chatbotContent.appendChild(messageDiv);
    chatbotContent.scrollTop = chatbotContent.scrollHeight; // Scroll to the latest message
}

function processBotResponse(userInput) {
    const activeContent = document.querySelector('.chatbot-content[style="display: block;"]');
    let responseMessage = "";

    // Mock Interview Service
    if (activeContent.id === 'mock-chatbot-content') {
        if (userInput.toLowerCase().includes("start")) {
            responseMessage = "What is the purpose of your visit to the United States?";
        } else if (userInput.toLowerCase().includes("business") || userInput.toLowerCase().includes("conference")) {
            responseMessage = "Great! You mentioned that your visit is for a business conference. Can you tell me more about the conference, such as the location, date, and your role in it?";
        } else if (userInput.toLowerCase().includes("tourism")) {
            responseMessage = "Got it! Could you tell me what places you plan to visit in the United States?";
        } else if (userInput.toLowerCase().includes("family")) {
            responseMessage = "Nice! Could you explain the nature of your visit to your family members in the U.S.?";
        } else {
            responseMessage = "Sorry, I didn't quite understand that. Can you please clarify or provide more details about your visit?";
        }

    }
    // Visa Requirements Service
    else if (activeContent.id === 'visa-requirements-content') {
        if (userInput.toLowerCase().includes("usa") || userInput.toLowerCase().includes("united states")) {
            responseMessage = "To apply for a U.S. visa, you will need to submit the DS-160 form, schedule a visa interview, pay the visa application fee, provide a valid passport, and submit any additional documents depending on the type of visa you are applying for.";
        }
        else if (userInput.toLowerCase().includes("visa appointment")) {
            responseMessage = "After completing the DS-160 form, you must schedule an appointment at the nearest U.S. embassy or consulate. The waiting time for appointments can vary depending on your location, so it's best to apply early.";
        }
        else if (userInput.toLowerCase().includes("ds-160")) {
            responseMessage = "The DS-160 is the online application form required for all U.S. visa applicants. You'll need to complete it and print the confirmation page to bring to your visa interview.";
        }
        else if (userInput.toLowerCase().includes("visa extension")) {
            responseMessage = "If you need to extend your stay in the U.S., you must apply for an extension before your current visa expires. This application must be submitted to the U.S. Citizenship and Immigration Services (USCIS) and include proof of your continued eligibility.";
        }
        else if (userInput.toLowerCase().includes("canada")) {
            responseMessage = "For Canada, you'll need your passport, application form, biometric information, and a proof of sufficient funds.\n\nFor Visitor Visa (Tourism): Invitation letter from a Canadian resident, travel itinerary, hotel booking, or flight reservation.";
        } else if (userInput.trim() !== "") {
            responseMessage = "Can you please tell me which country you're applying for so I can give you specific requirements?";
        } else {
            responseMessage = "Please tell me the country you're applying to so I can provide the specific visa requirements.";
        }

    }
    // Visa Guidance Service
    else if (activeContent.id === 'visa-guidance-content') {
        if (userInput.toLowerCase().includes("student")) {
            responseMessage = "To apply for a Canadian student visa (Study Permit), you will need: a letter of acceptance from a Designated Learning Institution (DLI), proof of financial support, passport-sized photos, and proof of no criminal record. You may also need to undergo a medical exam.";
        }
        else if (userInput.toLowerCase().includes("acceptance")) {
            responseMessage = "To apply for a Canadian student visa, you must first receive a letter of acceptance from a Designated Learning Institution (DLI) in Canada. This is one of the key requirements for your study permit application.";
        }
        else if (userInput.toLowerCase().includes("finance")) {
            responseMessage = "For a Canadian student visa, you will need to provide proof of sufficient funds to cover your tuition, living expenses, and return transportation. This can include bank statements, affidavits of support, or scholarship offers.";
        }
        
        else if (userInput.toLowerCase().includes("tourist")) {
            responseMessage = "For a tourist visa, you'll need a completed application form, passport-sized photos, and proof of your travel plans (like hotel bookings or flight tickets).";
        } else if (userInput.toLowerCase().includes("work")) {
            responseMessage = "For a work visa, your employer must provide an offer letter and sponsorship for the visa. You will also need proof of education, professional qualifications, and your passport.";
        } else if (userInput.trim() !== "") {
            responseMessage = "Could you specify what type of visa you are applying for so I can provide guidance tailored to that?";
        } else {
            responseMessage = "Please tell me the type of visa you are applying for (e.g., student, tourist, work).";
        }

    }
    // Document Authentication Service
    else if (activeContent.id === 'document-auth-content') {
        if (userInput.toLowerCase().includes("birth certificate")) {
            responseMessage = "For a birth certificate, make sure it's an official copy. If it's not in English, you will need a certified translation.";
        } else if (userInput.toLowerCase().includes("passport")) {
            responseMessage = "You will need to provide a clear, unaltered copy of your passport's information page.";
        } else if (userInput.toLowerCase().includes("marriage certificate")) {
            responseMessage = "Ensure your marriage certificate is an official copy. If not in English, you will need a certified translation.";
        } else {
            responseMessage = "Can you tell me more about the document you need authenticated so I can assist you further?";
        }
    }

    // If the active service is not recognized
    else {
        responseMessage = "Sorry, I couldn't recognize that request. Could you please clarify what you'd like help with?";
    }

    // Display the bot's response
    displayMessage(responseMessage, "bot");
}
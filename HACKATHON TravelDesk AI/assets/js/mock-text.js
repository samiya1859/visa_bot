
// Show and hide chatbot window
document.getElementById('mock-chatbot-button').onclick = function () {
    document.getElementById('chatbot-window').style.display = 'flex';
    document.getElementById('chatbot-button').style.display = 'none';
};

// Close the chatbot window
function closeChatbot() {
    document.getElementById('chatbot-window').style.display = 'none';
    document.getElementById('chatbot-button').style.display = 'flex';
}

// Send a message when user presses "Send" button
function sendMessage() {
    let userInput = document.getElementById('user-input').value;
    if (userInput.trim() !== "") {
        // Display user message
        displayMessage(userInput, "user");

        // Process and display bot response
        processBotResponse(userInput);
        document.getElementById('user-input').value = ""; // Clear input field
    }
}

// Display messages in the chatbot
function displayMessage(message, sender) {
    const chatbotContent = document.getElementById('mock-chatbot-content');
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', sender + '-message');
    messageDiv.innerHTML = `<p>${message}</p>`;
    chatbotContent.appendChild(messageDiv);
    chatbotContent.scrollTop = chatbotContent.scrollHeight; // Scroll to the latest message
}

// Process the user's input and generate bot responses
function processBotResponse(userInput) {
    const chatbotContent = document.getElementById('mock-chatbot-content');
    let responseMessage = "";

    if (userInput.toLowerCase().includes("I am applying for a US B-1 business visa. Can you help me with the interview practice?")) {
        responseMessage = "Absolutely! Let's begin with a few questions. Please answer each one to the best of your ability";
    }
    else if (userInput.toLowerCase().includes("Let's start.")) {
        responseMessage = "What is the purpose of your visit to the United States?";
    }
    else if (userInput.toLowerCase().includes("I don't know what to answer?")) {
        responseMessage = "Good! You mentioned that your visit is for a business conference. Make sure to provide details about the event, such as the date, location, and your specific role in it.";
    }
    // else if (userInput.toLowerCase().includes("help") || userInput.toLowerCase().includes("assistant")) {
    //     responseMessage = "How can I assist you today? Choose an option like 'Visa Status' or 'Document Checklist'.";
    // }
    else {
        responseMessage = "Sorry, I didn't quite understand. Could you ask something else?";
    }

    displayMessage(responseMessage, "bot");
}

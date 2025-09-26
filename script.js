// --- Page Scroll Karne Ke Liye Code ---
const startButton = document.querySelector('.scroll-down-btn');
const languageSection = document.querySelector('#language-choice');
startButton?.addEventListener('click', function(event) {
    event.preventDefault();
    languageSection.scrollIntoView({ behavior: 'smooth' });
});

// --- Language Buttons Ke Liye Naya Code ---
let currentLanguage = 'en'; // Default language English rakhi hai
const langButtons = document.querySelectorAll('.language-buttons button');
const chatbotSection = document.querySelector('#chatbot-section');

langButtons.forEach(button => {
    button.addEventListener('click', () => {
        // NAYA: Button se language code lena (jaise 'en', 'hi')
        currentLanguage = button.getAttribute('data-lang');
        console.log(`Language set to: ${currentLanguage}`);
        // Chatbot section tak scroll karna
        chatbotSection.scrollIntoView({ behavior: 'smooth' });
    });
});


// --- Aapka Purana Chatbot Logic (Thoda Sudhar Ke Saath) ---
const chatForm = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');
const chatMessages = document.getElementById('chat-messages');

// Form submit hone par
chatForm?.addEventListener('submit', (event) => {
    event.preventDefault();
    const userMessage = userInput.value.trim();
    if (userMessage) {
        appendMessage(userMessage, 'user-message');
        userInput.value = '';
        getBotReply(userMessage);
    }
});

// Message ko chat window mein jodna (Dono ke liye ek hi function)
function appendMessage(message, className) {
    const existingThinkingMessage = document.querySelector('.message.thinking');
    if (className === 'bot-message' && existingThinkingMessage) {
        existingThinkingMessage.innerText = message;
        existingThinkingMessage.classList.remove('thinking');
    } else {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', className);
        if (message === "Soch raha hoon...") {
            messageElement.classList.add('thinking');
        }
        messageElement.innerText = message;
        chatMessages.appendChild(messageElement);
    }
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Backend se jawaab laana
async function getBotReply(userMessage) {
    appendMessage("Soch raha hoon...", "bot-message");
    try {
        const response = await fetch('https://kisanchatbot.onrender.com', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            // NAYA: Ab hum sawaal ke saath language bhi bhej rahe hain
            body: JSON.stringify({ question: userMessage, language: currentLanguage }) 
        });
        const data = await response.json();
        appendMessage(data.answer, 'bot-message');

    } catch (error) {
        console.error("Error:", error);
        appendMessage("Sorry, kuch gadbad ho gayi. Kripya dobara koshish karein.", "bot-message");
    }
}
<template>
    <div class="chatbot-container">
        <button class="toggle-button" @click="toggleChatbot">
            <div v-if="!isOpen" id="icon-open"><i class="fa-regular fa-message"></i></div>
            <div v-else id="icon-close"><i class="fa-solid fa-minus"></i></div>
        </button>
        <div v-if="isOpen" class="chatbot">
            <div class="chat-window">
                <div v-for="(message, index) in messages" :key="index" class="message">
                    <p :class="{ 'user-message': message.from === 'user', 'bot-message': message.from === 'bot' }">
                        {{ message.text }}
                    </p>
                </div>
            </div>
            <div class="input-area">
                <input v-model="userInput" @keyup.enter="sendMessage" placeholder="Type your message here..." />
            </div>
        </div>
    </div>
</template>


<script>
import ChatbotService from "../services/chatbot.service";

export default {
    data() {
        return {
            isOpen: false,
            messages: [],
            userInput: '',
        };
    },
    methods: {
        toggleChatbot() {
            this.isOpen = !this.isOpen;
        },
        async sendMessage() {
            if (this.userInput.trim()) {
                this.messages.push({ text: this.userInput, from: 'user' });

                try {
                    const response = await ChatbotService.getMessageRasa({ message: this.userInput });
                    const botResponse = response.data.response || 'No response from server';
                    this.messages.push({ text: botResponse, from: 'bot' });
                } catch (error) {
                    console.error('Error:', error);
                    this.messages.push({ text: 'Error: Unable to get response from server', from: 'bot' });
                }

                this.userInput = '';
            }
        },
    },
};
</script>

<style scoped>

.chatbot-container {
    position: fixed;
    bottom: 20px;
    right: 20px;
}

#icon-open{
    font-size: 25px;
    padding: 10px;
}

.toggle-button{
    padding: 5px 10px 5px 10px;
    border: none;
    background-color: #007bff;
    color: white;
    cursor: pointer;
    border-radius: 50%;
    z-index: 100;
}

.chatbot {
    width: 350px;
    border: 1px solid #ccc;
    border-radius: 5px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    height: 450px;
}

.chat-window {
    flex: 1;
    overflow-y: auto;
    padding: 10px;
    background: #f9f9f9;
}

.input-area {
    display: flex;
}

input {
    flex: 1;
    padding: 10px;
    border: none;
}

.user-message {
    text-align: right;
    color: #1d72b8;
}

.bot-message {
    text-align: left;
    color: #333;
}
</style>

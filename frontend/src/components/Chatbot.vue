<template>
    <div class="chatbot-container">
        <button class="toggle-button" @click="toggleChatbot">
            <div v-if="!isOpen" id="icon-open"><i class="fa-regular fa-message"></i></div>
            <div v-else id="icon-close"><i class="fa-solid fa-minus"></i></div>
        </button>
        <div v-if="isOpen" class="chatbot">
            <div class="chatbot-header">Chatbot Hỗ Trợ</div>
            <div class="chat-window">
                <div v-for="(message, index) in messages" :key="index" class="message">
                    <div v-if="message.from === 'bot'" class="bot-message-container">
                        <img src="/logo.png" alt="Bot Avatar" class="bot-avatar" />
                        <p class="bot-message">{{ message.text }}</p>
                    </div>
                    <div v-else class="user-message">
                        <p style="margin:0px;">{{ message.text }}</p>
                    </div>
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

                await this.$nextTick(); // Đợi cập nhật DOM trước khi cuộn
                this.scrollToBottom();

                try {
                    const response = await ChatbotService.getMessageRasa({ message: this.userInput });
                    const botResponse = response.data.response || 'No response from server';
                    this.messages.push({ text: botResponse, from: 'bot' });

                    await this.$nextTick();
                    this.scrollToBottom(); // Cuộn xuống sau khi bot trả lời
                } catch (error) {
                    console.error('Error:', error);
                    this.messages.push({ text: 'Error: Unable to get response from server', from: 'bot' });

                    await this.$nextTick();
                    this.scrollToBottom();
                }

                this.userInput = '';
            }
        },
        scrollToBottom() {
            const chatWindow = this.$el.querySelector('.chat-window');
            chatWindow.scrollTop = chatWindow.scrollHeight;
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

#icon-open {
    font-size: 25px;
    padding: 10px 15px 10px 15px;
    background-color: #007bff;
    color: white;
    cursor: pointer;
    border-radius: 50%;
    z-index: 100;
}

#icon-close {
    position: absolute; 
    top: 20px;
    right: 10px; 
    font-size: 25px;
    padding: 10px; 
    cursor: pointer; 
    color: white;
    z-index: 100;
}


.toggle-button {
    border: none;
    background: none;
}

.chatbot-header{
    background-color: #007bff;
    color: white;
    padding: 10px;
    font-size: 18px;
    text-align: center; /* Căn giữa theo chiều ngang */
    font-weight: bold;
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
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

.bot-message-container {
    display: flex;
    align-items: flex-start;
    margin-bottom: 10px;
}

.bot-avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    margin-right: 10px;
}

.bot-message {
    background-color: #f0f0f0;
    padding: 10px;
    border-radius: 10px;
    color: #333;
    max-width: 70%;
}

.user-message {
    text-align: right;
    background-color: #1d72b8;
    color: white;
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 10px;
    max-width: 70%;
    margin-left: auto;
}

</style>

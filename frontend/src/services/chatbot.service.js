import createApiClient from "./api.chatbot.service";

class ChatbotService {
    constructor(baseUrl = "/api/chat/") {
        this.api = createApiClient(baseUrl);
    }
    async getMessageRasa(data) {
        console.log(data)
        const respone = await this.api.post("/", data);
        console.log("respione:", respone)
        return respone;
    }
}
export default new ChatbotService();
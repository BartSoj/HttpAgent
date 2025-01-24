# **mindAI**

**Intelligence for your robots, assistants, agents, and more.**

---

## 🚀 **Overview**

**mindAI** is a powerful AI-driven agent that can interact with any HTTP API, enabling seamless communication and
integration with the world. It can:

- Understand the world via **text** 💬, **audio** 🎙️, and **vision** 👀.
- Interact with the world through **audio playback** 🔈, **visual content** 🎬, and **platform integrations** 🤝.
- Continuously **run autonomously**, analyze real-time events, schedule tasks, and react to dynamic inputs.

With its rich API support, **mindAI** is your gateway to building intelligent, connected systems.

---

## 📌 **Key Features**

### Core Functionalities:

1. **Perception**:  
   Understands inputs via text, audio, and vision for comprehensive interaction.
2. **Action**:
    - Plays audio messages.
    - Displays visual content.
    - Integrates with diverse services and platforms.
3. **Autonomy**:  
   Operates continuously, reacting to real-time events, scheduling future actions, and performing tasks independently.

### API Integrations:

**Included APIs**:

- **Google Workspace**: Calendar, Chat, Docs, Drive, Gmail, Contacts, Apps Script, Sheets, Slides, Tasks.
- **Spotify Web API**: Seamless integration for managing and interacting with your Spotify account.

**Key APIs for Integration**:

- Wolfram Alpha
- Discord
- Notes, Calendar, and Reminders
- SSH API for computer control

**Planned Future Integrations**:

- **Apple Ecosystem**: Health, Fitness, Notes, Calendar, Reminders.
- **Google Services**: Maps, YouTube, Keep, Photos, Meet.
- **Home Automation**: Google Home, Tapo.
- **Communication**: WhatsApp, LinkedIn.
- **Business Tools**: Teams, Slack, GitHub.
- **Wellness**: Meditation and mental health platforms.
- **Education**: Canvas LMS.

---

## 🛠️ **Setup and Installation**

### Installing Dependencies:

Use `poetry` to install the required dependencies:

```bash
poetry install
```

### Setting API Keys:

Set your OpenAI API key:

```bash
export OPENAI_API_KEY=your_openai_api_key
```

### Running the Application:

1. **Start the HTTP Agent**:
   ```bash
   python src/agents.httpAgent/main.py
   ```  
2. **Start API Servers for Interaction**:
   ```bash
   python api_servers/server.py
   ```  

---

## 📚 **Documentation**

Detailed documentation is available in the `docs` directory for an in-depth understanding of core functionalities,
architecture, and integration options.

---

## 🌐 **API References**

To explore APIs for integration, you can refer to the following resources:

- [APIs.guru](https://apis.guru/)
- [API List.fun](https://apilist.fun/)
- [Public API Lists (GitHub)](https://github.com/public-api-lists/public-api-lists)

These platforms provide OpenAPI specifications and other documentation for countless APIs to power up your agent.

---

## 📝 **License**

This project is licensed under the [MIT License](LICENSE).  
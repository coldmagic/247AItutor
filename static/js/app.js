// Event listeners for subject buttons
const subjectButtons = document.querySelectorAll('.sidebar button');
const chatWindow = document.querySelector('.chat-window');
const form = document.querySelector('form');
const input = document.querySelector('input');
let askKateMode = false;

// Function to load chat history from the server based on the selected subject
function loadChatHistory(subject) {
  fetch(`/api/chats/${subject}`, { method: 'GET', headers: { 'Content-Type': 'application/json' } })
    .then((response) => response.json())
    .then((data) => {
      chatWindow.innerHTML = '';
      data.forEach((chat) => {
        addMessage('user', chat.message);
        addMessage('ai', chat.response);
      });
      console.log(data); // Print chat history in the console
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

// Update the event listeners for subject buttons
subjectButtons.forEach((button) => {
  button.addEventListener('click', () => {
    subjectButtons.forEach((btn) => btn.classList.remove('selected'));
    button.classList.add('selected');
    const subject = button.textContent;
    document.getElementById('subject-display').innerText = subject;
    loadChatHistory(subject);
  });
});

// Add submit event listener to the form
form.addEventListener('submit', (e) => {
  e.preventDefault();
  sendMessage();
});

// Function to add a message to the chat window
function addMessage(role, message) {
  const messageElement = document.createElement('div');
  let className = '';

  if (role === 'user') {
    className = 'user';
  } else if (role === 'ai') {
    className = 'ai';
  } else {
    className = 'system-message';
  }

  messageElement.classList.add('message', className);
  messageElement.textContent = message;
  chatWindow.appendChild(messageElement);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

// Function to get the currently selected subject
function getSelectedSubject() {
  const selectedButton = document.querySelector('.sidebar button.selected');
  return selectedButton ? selectedButton.textContent : '';
}

// Function to enable Ask KATE mode
function askKATE() {
  askKateMode = true;
  addMessage('system', 'Ask KATE Anything: KATE is ready for your question.');
}

// Function to send a message to the backend and receive KATE's response
function sendMessage() {
  const message = input.value.trim();
  if (message.length === 0) return;

  addMessage('user', message);
  fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ subject: getSelectedSubject(), message }),
  })
    .then((response) => response.json())
    .then((data) => {
      addMessage('ai', data.response);
    })
    .catch((error) => {
      console.error('Error:', error);
    });

  input.value = '';
}

// Function to load chat history from the server
function loadChatHistory() {
  fetch('/api/chats', { method: 'GET', headers: { 'Content-Type': 'application/json' } })
    .then((response) => response.json())
    .then((data) => {
      data.forEach((chat) => {
        addMessage('user', chat.message);
        addMessage('ai', chat.response);
      });
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

function logout() {
  window.location.href = '/logout';
}

const subjectButtons = document.querySelectorAll('.sidebar button');
const chatWindow = document.querySelector('.chat-window');
const form = document.querySelector('form');
const input = document.querySelector('input');
let askKateMode = false;

subjectButtons.forEach((button) => {
  button.addEventListener('click', () => {
    subjectButtons.forEach((btn) => btn.classList.remove('selected'));
    button.classList.add('selected');
    const subject = button.textContent;
    chatWindow.innerHTML = '';
    addMessage('system', `You are now chatting about ${subject}.`);
  });
});

form.addEventListener('submit', (e) => {
  e.preventDefault();
  sendMessage();
});

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

function getSelectedSubject() {
  const selectedButton = document.querySelector('.sidebar button.selected');
  return selectedButton ? selectedButton.textContent : '';
}

function askKATE() {
  askKateMode = true;
  addMessage('system', 'Ask KATE Anything: KATE is ready for your question.');
}

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

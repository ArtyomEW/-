// Переменные
let selectedUserId = null;  // Хранит ID пользователя, с которым мы общаемся в чате
let socket = null;          // Хранит объект WebSocket для соединения с сервером
let messagePollingInterval = null;  // Таймер для периодической загрузки сообщений

// Добавляем отдельную функцию для назначения обработчиков
function addUserClickListeners() {
    document.querySelectorAll('.user-item').forEach(item => {
        item.onclick = event => {
            const userItem = event.currentTarget;
            selectUser(
                userItem.getAttribute('data-user-id'), 
                userItem.textContent.trim(), 
                event
            );
        };
    });
}


// Функция для выхода из аккаунта
async function logout() {
    
        
            window.location.href = '/posts'; // Если все ок, перенаправляем на страницу авторизации
}    

// Выбор пользователя для общения
async function selectUser(userId, userName, event) {
    selectedUserId = userId;  // Запоминаем, с кем ведется беседа
    document.getElementById('chatHeader').innerHTML = `<span>Чат с ${userName}</span><button class="logout-button" id="logoutButton">Выход</button>`;
    document.getElementById('messageInput').disabled = false; // Активируем ввод сообщений
    document.getElementById('sendButton').disabled = false;   // Активируем кнопку отправки

    document.querySelectorAll('.user-item').forEach(item => item.classList.remove('active')); // Убираем выделение с других пользователей
    event.target.classList.add('active');  // Подсвечиваем текущего пользователя

    const messagesContainer = document.getElementById('messages');
    messagesContainer.innerHTML = '';  // Очищаем окно сообщений
    messagesContainer.style.display = 'block';  // Показываем окно сообщений

    document.getElementById('logoutButton').onclick = logout;  // Привязываем функцию выхода

    await loadMessages(userId);  // Загружаем предыдущие сообщения с этим пользователем
    connectWebSocket();  // Открываем WebSocket для обмена сообщениями в реальном времени
    startMessagePolling(userId);  // Начинаем периодически проверять новые сообщения
}

// Загрузка предыдущих сообщений
async function  loadMessages(userId) {
    try {
        const response = await fetch(`/chat/messages/${userId}`);  // Делаем запрос на сервер, чтобы получить старые сообщения
        const messages = await response.json();  // Преобразуем ответ в JSON

        const messagesContainer = document.getElementById('messages');
        messagesContainer.innerHTML = messages.map(message =>
            createMessageElement(message.content, message.sender_id)  // Используем sender_id вместо recipient_id
        ).join('');  // Склеиваем элементы и вставляем их в контейнер сообщений
    } catch (error) {
        console.error('Ошибка загрузки сообщений:', error);  // Ловим ошибки при загрузке
    }
}

// Соединение с WebSocket
function connectWebSocket() {
    if (socket) socket.close();  // Если соединение уже было, закрываем его

    socket = new WebSocket(`wss://${window.location.host}/chat/ws/${selectedUserId}`);  // Открываем новое WebSocket-соединение

    socket.onopen = () => console.log('WebSocket соединение установлено');  // Логируем успешное подключение

    socket.onmessage = (event) => {
        const incomingMessage = JSON.parse(event.data);
        if (incomingMessage.recipient_id === selectedUserId || incomingMessage.sender_id === selectedUserId) {
            addMessage(incomingMessage.content, incomingMessage.sender_id);  // Передаем sender_id
        }
    };

    socket.onclose = () => console.log('WebSocket соединение закрыто');  // Логируем закрытие соединения
}

// Отправка сообщения
async function sendMessage() {
    const messageInput = document.getElementById('messageInput');
    const message = messageInput.value.trim();  // Берем текст сообщения

    if (message && selectedUserId) {  // Проверяем, что сообщение не пустое и выбран собеседник
        const payload = {recipient_id: selectedUserId, content: message};  // Формируем данные для отправки

        try {
            await fetch('/chat/messages', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(payload)  // Отправляем сообщение на сервер
            });

            socket.send(JSON.stringify(payload));  // Также отправляем сообщение через WebSocket
            addMessage(message, selectedUserId);  // Добавляем сообщение в чат
            messageInput.value = '';  // Очищаем поле ввода
        } catch (error) {
            console.error('Ошибка при отправке сообщения:', error);  // Ловим ошибки
        }
    }
}

// Добавление нового сообщения в чат
function addMessage(text, sender_id) {
    const messagesContainer = document.getElementById('messages');
    messagesContainer.insertAdjacentHTML('beforeend', createMessageElement(text, sender_id));
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Формирование HTML-элемента для сообщения
function createMessageElement(text, sender_id) {
    const messageClass = sender_id === currentUserId ? 'my-message' : 'other-message';
    return `<div class="message ${messageClass}">${text}</div>`;
}

// Периодическая проверка новых сообщений
function startMessagePolling(userId) {
    clearInterval(messagePollingInterval);  // Очищаем старый таймер
    messagePollingInterval = setInterval(() => loadMessages(userId), 1000);  // Каждую секунду загружаем новые сообщения
}

// Привязка действий к элементам
document.querySelectorAll('.user-item').forEach(item => {
    item.onclick = event => selectUser(item.getAttribute('data-user-id'), item.textContent, event);  // Привязываем обработчик клика для выбора пользователя
});

document.getElementById('sendButton').onclick = sendMessage;  // Привязываем отправку сообщения на кнопку "Отправить"

document.getElementById('messageInput').onkeypress = async (e) => {
    if (e.key === 'Enter') {  // Если пользователь нажимает Enter в поле ввода сообщения
        await sendMessage();  // Отправляем сообщение
    }
};

async function fetchUsers() {
    try {
        const response = await fetch('/auth/users');
        const users = await response.json();
        const userList = document.getElementById('userList');

        userList.innerHTML = '';

        // Добавляем "Избранное"
        const favoriteElement = document.createElement('div');
        favoriteElement.classList.add('user-item');
        favoriteElement.setAttribute('data-user-id', currentUserId);
        favoriteElement.textContent = 'Избранное';
        userList.appendChild(favoriteElement);

        // Добавляем остальных пользователей
        users.forEach(user => {
            if (user.id !== currentUserId) {
                const userElement = document.createElement('div');
                userElement.classList.add('user-item');
                userElement.setAttribute('data-user-id', user.id);
                userElement.textContent = user.name;
                userList.appendChild(userElement);
            }
        });

        // Назначаем обработчики после обновления списка
        addUserClickListeners();
    } catch (error) {
        console.error('Ошибка при загрузке списка пользователей:', error);
    }
}


document.addEventListener('DOMContentLoaded', fetchUsers);
setInterval(fetchUsers, 10000); // Обновление каждые 10 секунд

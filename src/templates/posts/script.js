// script.js
const modal = document.getElementById("commentModal");
const span = document.getElementsByClassName("close")[0];

span.onclick = () => modal.style.display = "none";
window.onclick = (event) => {
    if (event.target == modal) modal.style.display = "none";
}

// Обработчик отправки комментария
document.getElementById("submitComment").addEventListener("click", async () => {
    const comment = document.getElementById("commentText").value.trim();
    const errorDiv = document.getElementById("modalError");
    const successDiv = document.getElementById("modalSuccess"); // Добавляем блок для успешных сообщений
    
    if (!comment) {
        errorDiv.textContent = "Комментарий не может быть пустым";
        return;
    }

    try {
        const userEmail = document.cookie
            .split('; ')
            .find(row => row.startsWith('email='))
            ?.split('=')[1];

        const response = await fetch(`/comments/add_comments/${currentPostId}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ 
                comment,
                user_email: userEmail
            }),
            credentials: "include"
        });

        if (!response.ok) throw new Error('Ошибка при отправке комментария');
        
        // Показываем сообщение об успехе
        successDiv.textContent = "Комментарий успешно добавлен!";
        errorDiv.textContent = "";
        
        // Очищаем поле ввода через 1 секунду
        setTimeout(() => {
            document.getElementById("commentText").value = "";
            successDiv.textContent = "";
            modal.style.display = "none";
            
            // Обновляем комментарии
            const commentsDiv = document.querySelector(`.comments[data-post-id="${currentPostId}"]`);
            if (commentsDiv) {
                commentsDiv.removeAttribute("data-loaded");
                const button = document.querySelector(`button[data-post-id="${currentPostId}"]`);
                if (button.textContent === "Скрыть комментарии") {
                    toggleComments(button); // Сначала закрываем
                    setTimeout(() => toggleComments(button), 100); // Затем открываем снова
                } else {
                    toggleComments(button); // Просто открываем
                }
            }
        }, 1000);

    } catch (error) {
        errorDiv.textContent = error.message;
        successDiv.textContent = "";
    }
});

// Исправленная функция toggleComments
function toggleComments(button) {
    const postElement = button.closest('.post');
    const commentsDiv = postElement.querySelector('.comments');
    const postId = button.dataset.postId;
    const isHidden = window.getComputedStyle(commentsDiv).display === 'none';

    // Всегда сбрасываем загруженные данные при открытии
    if (isHidden) {
        commentsDiv.removeAttribute('data-loaded');
        commentsDiv.innerHTML = '<div class="loader">Загрузка комментариев...</div>';
        commentsDiv.style.display = 'block';
        
        fetch(`/comments/get_comments/${postId}`)
            .then(response => {
                if (!response.ok) throw new Error('Ошибка загрузки комментариев');
                return response.json();
            })
            .then(comments => {
                commentsDiv.innerHTML = comments.length === 0 
                    ? '<div class="no-comments">Комментариев нет</div>'
                    : comments.map(comment => `
                        <div class="comment">
                            <strong>${comment.user_email}:</strong> ${comment.comment}
                        </div>
                    `).join('');
                commentsDiv.setAttribute('data-loaded', 'true');
                button.textContent = 'Скрыть комментарии';
            })
            .catch(error => {
                commentsDiv.innerHTML = `<div class="error">${error.message}</div>`;
            });
    } else {
        commentsDiv.style.display = 'none';
        button.textContent = 'Посмотреть комментарии';
    }
}

function toggleCommentForm(button) {
    const form = button.nextElementSibling;
    form.style.display = form.style.display === 'none' ? 'block' : 'none';
    button.textContent = form.style.display === 'none' 
        ? 'Добавить комментарий' 
        : 'Отмена';
}

async function submitComment(form, postId) {
    const commentInput = form.querySelector('.comment-input');
    const errorDiv = form.querySelector('.error');
    const commentText = commentInput.value.trim();

    if (!commentText) {
        errorDiv.textContent = 'Комментарий не может быть пустым';
        return;
    }

    try {
        const response = await fetch(`/add_comments/${postId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                comment: commentText
            }),
            credentials: 'include'
        });

        if (!response.ok) throw new Error('Ошибка при отправке комментария');
        
        commentInput.value = '';
        errorDiv.textContent = '';
        form.style.display = 'none';
        form.previousElementSibling.textContent = 'Добавить комментарий';
        
        // Обновляем список комментариев
        const commentsDiv = form.parentElement.querySelector('.comments');
        commentsDiv.removeAttribute('data-loaded');
        if (commentsDiv.style.display !== 'none') {
            commentsDiv.innerHTML = '<div class="loader">Обновление комментариев...</div>';
            toggleComments(form.parentElement.querySelector('.toggle-btn'));
        }
    } catch (error) {
        errorDiv.textContent = error.message;
    }
}

// Изменения в функции renderPosts
function renderPosts(posts) {
    const container = document.getElementById("posts-container");
    container.innerHTML = "";
    
    posts.forEach(post => {
        const postHTML = `
        <div class="post">
            <div class="post-content">
                <h2>${post.name}</h2>
                <p class="user-info">Автор: 
                    <a href="/user/${post.user_id}" class="author-link">
                        ${post.user_email}
                    </a>
                </p>
                <img src="static/photo/${post.file_name}" alt="Изображение поста">
                <p>${post.description}</p>
                
                <div class="buttons-container">
                    <button class="toggle-btn" onclick="toggleComments(this)" data-post-id="${post.id}">
                        Посмотреть комментарии
                    </button>
                    <button class="add-comment-btn" onclick="openCommentModal(${post.id})">
                        Добавить комментарий
                    </button>
                </div>
                <div class="comments" style="display: none;" data-post-id="${post.id}"></div>
            </div>
        </div>
        `;
        container.innerHTML += postHTML;
    });
}

function openCommentModal(postId) {
    currentPostId = postId;
    modal.style.display = "block";
}

// Остальной код без изменений
// Загрузка постов
fetch('/posts/get_all_posts')
    .then(response => {
        if (!response.ok) throw new Error('Ошибка сети');
        return response.json();
    })
    .then(renderPosts)
    .catch(error => {
        console.error('Ошибка:', error);
        document.getElementById('posts-container').innerHTML = `
            <div class="error">Ошибка загрузки постов: ${error.message}</div>
        `;
    });

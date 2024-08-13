const eventSource = new EventSource("api/stream-chat-events/")

eventSource.onopen = function() {
    console.log("Connection established")
}

eventSource.onmessage = function(e) {
    const data = JSON.parse(e.data)
    console.log(data)
    if (data.action == 'create') {
        const message = {...data.message}
        message.timestamp = formatDate(message.timestamp + 'Z') // add 'Z' to make it UTC
        renderMessage(message)
    } else if (data.action == 'delete') {
        $(`.message#${data.message_id}`).remove()
    } else if (data.action == 'typing') {
        renderTypingUsers(data.users)
    }
}

function renderMessage(message){
    if (!$(`.message#${message.id}`).length) { // check if message already exists
        let messageElement = $('<div class="message">')
        .prop('id', message.id)
        .append($('<div class="message-info">')
            .append(`<img src="${message.author.pfp}" alt="Avatar">`)
            .append(`<span class="message-author">${message.author.username}</span>`)
            .append(`<span class="timestamp">${message.timestamp}</span>`)
        )

        .append($('<p class="message-text">')
            .text(message.text)
        )

        if (message.author.username == username) {
            messageElement.addClass('own-message')
            .find('.message-info').append(
                $('<div class="delete-message">')
                    .on('click', ()=>{ deleteMessage(message.id) })
                    .append('<img src="/static/icons/remove.svg">')
            )
        }

        $('#chat-messages').append(messageElement)
        messageElement[0].scrollIntoView()
    }
}

function deleteMessage(messageId) {
    $.post( `/api/delete-message/`, {
        'message_id': messageId,
        'csrfmiddlewaretoken': csrftoken
    }, () => {
        $(`.message#${messageId}`).remove()
    })
}

// Send message
$('#message-form').on('submit', function(event) {
    event.preventDefault() // Prevent the form from submitting the traditional way
    let text = $('#message-input').val()
    if (text.trim()) { // check if message text is not empty
        $.post(location.href, {
            'text': text,
            'csrfmiddlewaretoken': csrftoken
        }, () => {
            $('#message-input').val('') // Clear the message input
        })
    }
});

// Typing status
let typingTimeout
let typingStatus = false
$('#message-input').on('input', function(event) {
    const text = $(this).val()
    clearTimeout(typingTimeout)
    if (!typingStatus && text) {
        sendTypingStatus(true)
    }
    typingTimeout = setTimeout(() => {
        if (typingStatus) {
            sendTypingStatus(false)
        }
    }, 10000) // send not typing status after 10 seconds
})

function sendTypingStatus(isTyping) {
    typingStatus = isTyping
    $.post('api/set-typing-status/', {
        'csrfmiddlewaretoken': csrftoken,
        'is_typing': isTyping
    })
}

function renderTypingUsers(users) {
    if (users.length==1) {
        $('#typing-users').text(`${users[0]} is typing...`)
    } else if (users.length == 2) {
        $('#typing-users').text(`${users[0]} and ${users[1]} are typing...`)
    } else if (users.length > 2) {
        $('#typing-users').text(`${users.join(', ')} are typing...`)
    }
        else {
        $('#typing-users').text(' ')
    }
}
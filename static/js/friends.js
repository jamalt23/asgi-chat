// friend requests
$('.friend-request button').on('click', function(e) {
    const fromUser = $(this).parent().find('span').text()
    const action = $(this).text().toLowerCase()
    $.post( `/api/${action}-friend-request/`, {
        'from_user': fromUser,
        'csrfmiddlewaretoken': csrftoken
    }, () => {
        $(this).parent().remove()
        if (action == 'accept') { 
            let friendElement = $(`<li class="friend">`)
            .append(`<span>${fromUser}</span>`)
            .append($(`<button class="btn-unfriend">Unfriend</button>`)
                .on('click', unfriend))

            $('.friend-list').append(friendElement)
            $('#no-friends').hide()
        }
    })
})

// unfriend
$('.btn-unfriend').on('click', unfriend); function unfriend(e) {
    const friend = $(this).parent().find('span').text()
    $.post( `/api/unfriend/`, {
        'friend': friend,
        'csrfmiddlewaretoken': csrftoken
    }, () => {
        $(this).parent().remove()
    })
}
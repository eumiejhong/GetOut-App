let user = document.getElementById("story-user");
const userID = $(user).data('id');
const userTimestamp = $(user).data('time');
let el = document.getElementById("comment-form");
const storyID = $(el).data('id');
const storyType = $(el).data('type');

async function processCommentForm(evt){
    evt.preventDefault();
    let body = document.getElementById("comment-body").value;
    const commentType = storyType == 'rec_park' ? 'rec-park-story' : 'campsite-story'

    const response = await axios.post(`/site/${storyID}/add-comment`, {
        body,
        storyID,
        userID,
        userTimestamp
    });
    let html = generateCommentHTML(response.data.comment)
    let newComment = $(html);
    $("#comment-area").append(newComment);
    $("#comment-form").trigger("reset")
}

function generateCommentHTML(comment) {
    return `
        <p>${comment.body} by: ${comment.username} on: ${comment.timestamp}</p>
    `
}

async function showInitialComments() {
    const response = await axios.get(`/site/${storyID}/show-comments`)
    //console.log(response)
    for(let commentResponse of response.data.comments) {
        //console.log(commentResponse)
        let newComment = $(generateCommentHTML(commentResponse));
        $("#comment-area").append(newComment);
    }
}

$(function(){
    showInitialComments();
    $("#comment-form").on('submit', processCommentForm)
})

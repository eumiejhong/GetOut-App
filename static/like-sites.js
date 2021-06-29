$(function(){
    const TRUE = 'true';
    const FALSE = 'false';

    $(window).click(async function(e){
        let el = null;
        if (e.target.matches('.like-btn')){
            el = e.target;
        } else if ($(e.target).closest('.like-btn')){
            el = $(e.target).closest('.like-btn');
        }

        if (!el){
            return;
        }

        //console.log(el)
        const isLiked = $(el).data('liked') === TRUE;
        //console.log(isLiked)
        const action = isLiked ? 'unlike' : 'like';
        //console.log(action)
        const ID = $(el).data('object-id');
        //console.log(ID)
        const $heartIcon = $(el).find('.fa-heart');

        if (!ID) {
            return;
        }


        
        await axios.post(`/site/${action}/${ID}`);
        //console.log(response)
        
        if (isLiked) {
            // Unliking it
            $heartIcon.removeClass('fas').addClass('far');
            $(el).data('liked', FALSE)
        } else {
            $heartIcon.addClass('fas').removeClass('far');
            $(el).data('liked', TRUE);
        }
    });
})
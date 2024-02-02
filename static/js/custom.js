function sendArticleComment(articleId) {
    var comment = $('#commentText').val();
    var parentId = $('#parent_id').val();
    // console.log(parentId);
    $.get('/articles/add-article-comment', {
        article_comment: comment,
        article_id: articleId,
        parent_id: parentId
    }).then(res => {
        $('#comment_area').html(res);
        $('#commentText').val('');
        $('#parent_id').val('');
        if(parentId !== null && parentId !== '')
            document.getElementById('single_comment_'+ parentId).scrollIntoView({behavior:"smooth"});
        else
            document.getElementById('comment_area').scrollIntoView({behavior:"smooth"});


    });
}

function fillParentId(parentId){
    $('#parent_id').val(parentId);
    document.getElementById('comment_form').scrollIntoView({behavior:"smooth"});
}


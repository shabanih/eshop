function sendArticleComment(articleId){
    // console.log('custom js')
    var comment = $('#commentText').val();
    $.get('/add_article_comment', {
        articleComment: comment,
        article_id: articleId,
        parent_id: null
    }).then(res=>{
        console.log(res)
    });
}

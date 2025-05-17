


function set_article_info_data(obj, article_slug_id){

    document.getElementById(`word_count_${article_slug_id}`).textContent = obj.data[0].word_count ?? "N/A";
    document.getElementById(`image_count_${article_slug_id}`).textContent = obj.data[0].image_count ?? "N/A";
    document.getElementById(`heading_count_${article_slug_id}`).textContent = obj.data[0].heading_count ?? "N/A";
    
    document.getElementById(`total_paragraphs_${article_slug_id}`).textContent = obj.data[0].total_paragraphs ?? "N/A";
    document.getElementById(`long_paragraphs_${article_slug_id}`).textContent = obj.data[0].long_paragraphs ?? "N/A";
    document.getElementById(`short_paragraphs_${article_slug_id}`).textContent = obj.data[0].short_paragraphs ?? "N/A";
    document.getElementById(`medium_paragraphs_${article_slug_id}`).textContent = obj.data[0].medium_paragraphs ?? "N/A";

    document.getElementById(`total_sentences_${article_slug_id}`).textContent = obj.data[0].total_sentences ?? "N/A";
    document.getElementById(`long_sentences_${article_slug_id}`).textContent = obj.data[0].long_sentences ?? "N/A";
    document.getElementById(`short_sentences_${article_slug_id}`).textContent = obj.data[0].short_sentences ?? "N/A";
    document.getElementById(`medium_sentences_${article_slug_id}`).textContent = obj.data[0].medium_sentences ?? "N/A";
    document.getElementById(`passive_sentences_${article_slug_id}`).textContent = obj.data[0].passive_sentences ?? "N/A";

}
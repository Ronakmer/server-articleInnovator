

function domain_article_chart(domain_console_data, slug_id){

    domain_console_data.then((response) => {
        console.log(response,'xxxxx')
        // console.log(response.metrics_data.total_publish,'xxxxx')

        const total_draft = document.getElementById(`total_draft_${slug_id}`);
        const total_publish = document.getElementById(`total_publish_${slug_id}`);
        const total_scheduled = document.getElementById(`total_scheduled_${slug_id}`);

        const metrics_data = response?.metrics_data || {};


        if (total_draft) {
            total_draft.textContent = metrics_data.total_draft || 0;
        }

        if (total_scheduled) {
            total_scheduled.textContent = metrics_data.total_scheduled || 0;
        } 

        if (total_publish) {
            total_publish.textContent = metrics_data.total_publish || 0;
        } 

    })
}
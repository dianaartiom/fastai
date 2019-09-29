$('#submit').click(function() {
    event.preventDefault();
    var form_data = new FormData($('#uploadform')[0]);
    $.ajax({
        type: 'POST',
        url: '/uploadajax',
        data: form_data,
        contentType: false,
        processData: false,
        dataType: 'json'
    }).done(function(data, textStatus, jqXHR){
        console.log(data);
        console.log(textStatus);
        console.log(jqXHR);
        console.log('Success!');
        $("#resultFilename").text(data['name']); // name of the file
        $("#resultFilesize").text(data['size']); // size of the file
        //my_url = "{{ url_for('upload', filename="+data['name']+" }}";
        $("#image").attr('src', '/static/'+data['path']);
        $("#adv-btn").attr('value', data['name']);
        $("#adv-btn").show();
        //get_image(data['name'])
    }).fail(function(data){
        alert('error!');
    });
});


$("#enviar").click(function(){
    $.get("https://www.themealdb.com/api/json/v1/1/categories.php", function(data){
        var count = 0;
        $.each(data.categories, function(i, item){
            if (count < 4) {
                $("#categorias").append("<tr><td>"+item.idCategory+"</td><td>"+item.strCategory +
                                         "</td><td><img src='"+item.strCategoryThumb+"'>"); 
                count++;
            } else {
                return false;
            }                              
        });
    });
});
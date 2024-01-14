
function add_hour(){
    var flight_hour = document.getElementById("flight_hour");
    for (var i = 0; i<=23; i=i+1){
        if (i == 0){
            var text = "12:00am";
        } else if (i>=1 && i <= 11){
            var text  = i.toString() + ":00am";
        } else if (i == 12){
            var text = "12:00pm";
        } else{
            var t = i - 12;
            var text = t.toString() + ":00pm";
        }

        var option = document.createElement('option');
        option.text = text;
        option.value = i;
        flight_hour.add(option, 0);
    }

}

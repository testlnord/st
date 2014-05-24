/**
 * Created by arkady on 5/24/14.
 */
$("button[name='log']").click(function(){
    var gamid;
    gamid_ = $(this).attr("data-gameid");
    $.get("/game_log/", {gamid: gamid_ }, function(data){
        $('#game_log').html(data);
        $('#game_log').show();
    });
});

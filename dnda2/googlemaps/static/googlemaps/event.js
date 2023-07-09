function live_p(){
    live_preview = document.getElementById('flexSwitchCheckDefault').checked
    if(live_preview){
        document.getElementById('video-screen').style = 'position: absolute;right: 0;display: flex;align-items: center;justify-content:center;' 
    }
    else{
        document.getElementById('video-screen').style = 'display: none;' 
    }
}
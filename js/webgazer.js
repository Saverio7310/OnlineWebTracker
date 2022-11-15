/* WebGazer.js library */

//with this you can save all data and when you reopen the tracker it will remember it
window.saveDataAcrossSessions = false

//this is used to tell the html page that there are a lot of data to read and that this process is fast. This will optimize the gathering of the data
const canvas = document.createElement('canvas');
const ctx = canvas.getContext('2d', {willReadFrequently: true});

var start_record = false
var i = 0
var data_array = []

/* webgazer.setGazeListener((data, timestamp) => {

    //elapsed time is based on time since begin was called
    //setInterval(console.log(data, "timestamp is ", timestamp), 20)

    //it saves the coordinates and the timestamps of the tracking dots until you press again the button "start record"
    if (start_record) {
        var data_obj = new Object()
        data_obj.x = data.x
        data_obj.y = data.y
        data_obj.time = timestamp
        data_array[i] = data_obj
        i++
        setTimeout(100)
    }

    }).begin() */


    webgazer.setGazeListener(function(data, elapsedTime) {
        if (data == null) {
            return;
        }
        var xprediction = data.x; //these x coordinates are relative to the viewport
        var yprediction = data.y; //these y coordinates are relative to the viewport
        //console.log(elapsedTime); //elapsed time is based on time since begin was called
    }).begin();


//it's used to stop the tracker
pause = function() {
    webgazer.pause()
    console.log("Pause")
}

//it's used to resume the tracker
resume = function() {
    webgazer.resume()
    console.log("Resume")
}

var index_image = 0
let img_array = ["Griglia.png", "text.png", "task.png", "dv1.png", "dv2.png", "dv3.png", "dv4.png"]

previous = function() {
    if (index_image > 0) {
        index_image--
        document.getElementById("img").src = "..\\img\\" + img_array[index_image]
    }
}

next = function() {
    if (index_image < 6) {
        index_image++
        document.getElementById("img").src = "..\\img\\" + img_array[index_image]
    }
}

//used to start and stop the acquisition of the data. When you stop it, it will save in a csv file all the data gathered before and download it
start = function() {
    if (start_record === false) {
        start_record = true
    } else {
        start_record = false
        let csvContent = "x,y,timestamp" + "\r\n"
        data_array.forEach((element) => {
            console.log(element)
            let row = element.x + "," + element.y + "," +element.time
            csvContent += row + "\r\n"
        })
        data_array = []

        var hiddenElement = document.createElement('a');  
        hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(csvContent);  
        hiddenElement.target = '_blank';  
          
        //provide the name for the CSV file to be downloaded  
        hiddenElement.download = 'GazeData.csv';  
        hiddenElement.click();  

        /*
        var encodedUri = encodeURI(csvContent)
        window.open(encodedUri)
        
        var encodedUri = encodeURI(csvContent);
        var link = document.createElement("a");
        link.setAttribute("href", encodedUri);
        link.setAttribute("download", "dati.csv");
        document.body.appendChild(link); 
        link.click();
        */
    }
    console.log("Premuto tasto", start_record)
}

//unused for now
chart = function() {
    
}
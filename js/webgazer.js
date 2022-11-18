/* WebGazer.js library */

//with this you can save all data and when you reopen the tracker it will remember it
window.saveDataAcrossSessions = false

//this is used to tell the html page that there are a lot of data to read and that this process is fast. This will optimize the gathering of the data
const canvas = document.createElement('canvas');
//CanvasRenderingContext2D.willReadFrequently = true
const ctx = canvas.getContext('2d', { willReadFrequently: true });

var start_record = false
var i = 0
var data_array = []

webgazer.setRegression("ridge")

webgazer.setGazeListener((data, timestamp) => {

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

}).saveDataAcrossSessions(false)
    .begin()

/*
webgazer.setGazeListener(function (data, elapsedTime) {
    if (data == null) {
        return;
    }
    var xprediction = data.x; //these x coordinates are relative to the viewport
    var yprediction = data.y; //these y coordinates are relative to the viewport
    //console.log(elapsedTime); //elapsed time is based on time since begin was called
}).begin();
*/


//it's used to stop the tracker
pause = function () {
    webgazer.pause()
    console.log("Pause")
}

//it's used to resume the tracker
resume = function () {
    webgazer.resume()
    console.log("Resume")
}

var index_image = 0
let img_array = ["griglia", "text", "task", "dv1", "dv2", "dv3", "dv4"]

previous = function () {
    if (index_image > 0) {
        index_image--
        document.getElementById("img").src = "..\\img\\" + img_array[index_image] + ".png"
    }
}

next = function () {
    if (index_image < 6) {
        index_image++
        document.getElementById("img").src = "..\\img\\" + img_array[index_image] + ".png"
    }
}

//used to start and stop the acquisition of the data. When it's stopped, the system will save in a csv file all the data gathered before and download it
start = function () {
    start_record = !start_record

    if (start_record)
        document.getElementById("logo").src = "..\\img\\play.png"
    else {
        document.getElementById("logo").src = "..\\img\\pause.png"

        let csvContent = "x,y,timestamp" + "\r\n"
        data_array.forEach((element) => {
            console.log(element)
            let row = element.x + "," + element.y + "," + element.time
            csvContent += row + "\r\n"
        })
        data_array = []

        var hiddenElement = document.createElement('a');
        hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(csvContent);
        hiddenElement.target = '_blank';

        //provide the name for the CSV file to be downloaded  
        hiddenElement.download = img_array[index_image] + ".csv";
        hiddenElement.click();

        document.getElementById('textInput').value = ''
    }
}
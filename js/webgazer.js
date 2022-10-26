/* WebGazer.js library */

//with this you can save all data and when you reopen the tracker it will remember it
window.saveDataAcrossSessions = false

//this is used to tell the html page that there are a lot of data to read and that this process is fast. This will optimize the gathering of the data
const canvas = document.createElement('canvas');
const ctx = canvas.getContext('2d', {willReadFrequently: true});

var start_record = false
var i = 0
var data_array = []

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

    }).begin()

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

//used to start and stop the acquisition of the data. When you stop it, it will save in a csv file all the data gathered before and download it
start = function() {
    if (start_record === false) {
        start_record = true
    } else {
        start_record = false
        let csvContent = "data:text/csv;charset=utf-8," + "\r\n" + "x,y,timestamp" + "\r\n"
        data_array.forEach((element) => {
            console.log(element)
            let row = element.x + "," + element.y + "," +element.time
            csvContent += row + "\r\n"
        })
        data_array = []

        var encodedUri = encodeURI(csvContent)
        window.open(encodedUri)
        /*
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
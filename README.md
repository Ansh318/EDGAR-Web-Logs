# EDGAR-Web-Logs

# Background 

In this project, I have built a command line tool for processing compressed EDGAR web logs. In the US, public companies need to regularly file various statements and reports to the Securities and Exchange Commission's EDGAR database. EDGAR data is publicly available online; furthermore, web requests to EDGAR from around the world are logged and published. The logs list the pages visited and weakly anonymized IP addresses of visitors, allowing good guesses about what docs various hedge funds and others are looking at. EDGAR logs are huge. Logs for just one day might be about 250 MB compressed as a .zip or 2 GB uncompressed. It will be very useful to have command line tools to sample and otherwise process this data. Your tool will have two commands for dealing with these zips: sample and country and will also provide three commands for visualizing where web requests to EDGAR are originating: geocontinent, geohour, and video. 


# Overview 

### 1. `sample` Command

This one takes three arguments:
* input zip
* output zip
* stride

If stride is 10, then rows 0, 10, 20, 30, etc. will be in the sample.
If stride is 100, then 0, 100, 200, 300, etc. will be in the sample.

For this command (and those following), there won't always be enough
memory to read the entire CSV in with Pandas, so you should use
Python's `csv` module for looping over one row at a time.

### 2. `country` Command

This command has two parts: sorting and adding a new country column.

### 3. `video` Command

Imagine running `geohour` for all hours of the day, then combining the
images to make a video.  That's basically what this command does.

We'll be using [FuncAnimation](https://matplotlib.org/3.2.0/api/_as_gen/matplotlib.animation.FuncAnimation.html#matplotlib.animation.FuncAnimation)
to create the video, then call [.to_html5_video(...)](https://matplotlib.org/api/_as_gen/matplotlib.animation.Animation.to_html5_video.html).

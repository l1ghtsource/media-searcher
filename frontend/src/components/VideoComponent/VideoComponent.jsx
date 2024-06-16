import React, { useEffect, useRef, useState, useCallback } from 'react';
import cl from './VideoComponent.module.css';
import volume from "../../assets/svgIcons/volume.svg";
import mute from "../../assets/svgIcons/mute.svg";
import play from "../../assets/svgIcons/play.svg";
import pause from "../../assets/svgIcons/pause.svg";
// import transcriptionImg from "../../assets/svgIcons/transcription.svg"
import descriptionImg from "../../assets/svgIcons/description.svg";
import filter from "../../assets/svgIcons/filter.svg"
import AddVideoBtn from '../AddVideoBtn/AddVideoBtn';
import FiltersMobileComponent from '../FiltersMobileComponent/FiltersMobileComponent';
import DescriptionMobile from '../DescriptionMobile/DescriptionMobile';
// import TranscriptionInput from '../TranscriptionInput/TranscriptionInput';

function VideoComponent({ 
  videoInfo,
  id, 
  onPlay, 
  selectedOptions, 
  toggleOption, 
  faces, 
  filters, 
  isFilters, 
  isTranscription, 
  onToggleFilters, 
  onToggleTranscription, 
  isDescription, 
  onToggleDescription 
}) {
  const {url, description, facesVideo, cluster} = videoInfo;
  const videoRef = useRef(null);
  const [isPlaying, setIsPlaying] = useState(true);
  const [isMuted, setIsMuted] = useState(false);
  const [duration, setDuration] = useState(0);
  const [currentTime, setCurrentTime] = useState(0);
  const [progressPercent, setProgressPercent] = useState(0);
  const requestRef = useRef(null);

  useEffect(() => {
    const video = videoRef.current;

    const handleLoadedMetaData = () => {
      setDuration(video.duration);
    };

    const handleTimeUpdate = () => {
      setCurrentTime(video.currentTime);
      setProgressPercent((video.currentTime / video.duration) * 100);
    };
    
    video.addEventListener('loadedmetadata', handleLoadedMetaData);
    video.addEventListener('timeupdate', handleTimeUpdate);

    return () => {
      video.removeEventListener('loadedmetadata', handleLoadedMetaData);
      video.removeEventListener('timeupdate', handleTimeUpdate);
    };
  }, []);

  const animate = useCallback(() => {
    const video = videoRef.current;
    if (video) {
      setCurrentTime(video.currentTime);
      setProgressPercent((video.currentTime / video.duration) * 100);
      requestRef.current = requestAnimationFrame(animate);
    }
  }, []);

  useEffect(() => {
    if (isPlaying) {
      requestRef.current = requestAnimationFrame(animate);
    } else {
      cancelAnimationFrame(requestRef.current);
    }

    return () => cancelAnimationFrame(requestRef.current);
  }, [isPlaying, animate]);

  const togglePlayPause = () => {
    const video = videoRef.current;
    if (isPlaying) {
      video.pause();
    } else {
      video.play();
      if (onPlay){
        onPlay();
      }
    }
    setIsPlaying(!isPlaying);
  };

  const toggleMute = () => {
    const video = videoRef.current;
    video.muted = !isMuted;
    setIsMuted(!isMuted);
  };

  const handleProgressChange = (event) => {
    const video = videoRef.current;
    const newTime = event.target.value;
    video.currentTime = newTime;
    setCurrentTime(newTime);
    setProgressPercent((newTime / video.duration) * 100);
  };

  return (
    <div className={cl.videoContainer}>
      <div className={cl.wrapper}>
        <ul className={cl.videoControls}>
          <li className={cl.options}>
            <button className={cl.play} onClick={togglePlayPause}>
              <img src={isPlaying ? pause : play} alt="play/pause" />
            </button>
            <button className={cl.volume} onClick={toggleMute}>
              <img src={isMuted ? mute : volume} alt="volume" />
            </button>
          </li>
        </ul>
        <div className={cl.progressContainer}>
          <input
            type="range"
            className={cl.progressBar}
            min="0"
            max={duration}
            value={currentTime}
            onChange={handleProgressChange}
            style={{
              background: `linear-gradient(90deg, rgba(153, 153, 153, 0.4) ${progressPercent}%, rgba(0, 0, 0, 0.4) ${progressPercent}%)`
            }}
          />
        </div>
      </div>
      <div className={cl.addVideo}>
          <AddVideoBtn/>
      </div>
      <div className={cl.video__btn}>
          {/* <div className={isTranscription ? `${cl.videoBtn} ${cl.active}` : cl.videoBtn}>
            <img src={transcriptionImg} alt="transcription" onClick={onToggleTranscription}/>
          </div> */}
          <div className={isDescription ? `${cl.videoBtn} ${cl.active}` : cl.videoBtn}>
            <img src={descriptionImg} alt="description" onClick={onToggleDescription} />
          </div>
          <div className={isFilters ? `${cl.videoBtn} ${cl.active}` : cl.videoBtn}>
            <img src={filter} alt="filter" onClick={onToggleFilters} />
          </div>
      </div>
      <video id={id} className={cl.video} loop preload='metadata' src={url} ref={videoRef} onClick={togglePlayPause} playsInline>
        Простите, но ваш браузер не поддерживает встроенные видео.
        Попробуйте скачать видео <a href={url}>по этой ссылке</a>
        и открыть его на своём устройстве.
      </video>
      {
        isFilters && (
          <div className={cl.filtersMobile}>
            <FiltersMobileComponent filters={filters} selectedOptions={selectedOptions} toggleOption={toggleOption} faces={faces}/>
          </div>
        )
      }
      {/* {
        isTranscription && (
          <div className={cl.transcriptionMobile}>
            <TranscriptionInput url={url}/>
          </div>
        )
      } */}
      {
        isDescription && (
          <div className={cl.descriptionMobile}>
            <DescriptionMobile description={description} faces={facesVideo} cluster={cluster}/>
          </div>
        )
      }
    </div>
  );
}

export default VideoComponent;

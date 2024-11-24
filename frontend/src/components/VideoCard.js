import React from "react";

const VideoCard = ({ videoSrc, onViewArticle }) => {
    return (
        <div className="relative h-full w-full snap-center">
            <video
                className="relative h-screen object-cover"
                src={videoSrc}
                controls="false"
                type="video/mp4"
            >
                Your browser does not support the video tag.
            </video>
            <div className="absolute bottom-0 right-0 mb-[350px]">
                <div className="p-10 flex gap-y-8 flex-col justify-center">
                    <button
                        className="bg-orange-400 opacity-60 hover:opacity-100 w-16 h-16 p-3 text-white font-bold rounded-full shadow-md transition-colors duration-300 text-black"
                    >
                        <img src="https://cdn-icons-png.flaticon.com/512/151/151910.png" />
                    </button>
                    <button
                        className="bg-orange-400 opacity-60 hover:opacity-100 w-16 h-16 p-3 text-white font-bold rounded-full shadow-md transition-colors duration-300 text-black"
                    >
                        <img src="https://cdn-icons-png.flaticon.com/512/1380/1380338.png" />
                    </button>
                    <button
                        onClick={onViewArticle}
                        className="bg-orange-400 opacity-60 hover:opacity-100 w-16 h-16 p-3 text-white font-bold rounded-full shadow-md transition-colors duration-300 text-black"
                    >
                        <img src="https://cdn-icons-png.flaticon.com/512/9293/9293723.png" />
                    </button>
                </div>

            </div>

        </div >
    );
};



export default VideoCard;

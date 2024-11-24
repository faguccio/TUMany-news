import React from "react";

const VideoCard = ({ videoSrc, onViewArticle }) => {
    return (
        <div className="relative h-screen snap-center">
            <video
                className="relative overflow-x-hidden h-full object-cover"
                src={videoSrc}
                controls="false"
                type="video/mp4"
            >
                Your browser does not support the video tag.
            </video>
            <div className="absolute bottom-0 right-0 mb-8">
                <div className="p-8 flex justify-center">
                    <button
                        onClick={onViewArticle}
                        className="bg-white hover:bg-gray-300 w-20 h-20 px-6 text-white font-bold rounded-full shadow-md transition-colors duration-300 text-black"
                    >
                        <img src="https://cdn-icons-png.flaticon.com/512/9293/9293723.png" />
                    </button>
                </div>

            </div>

        </div >
    );
};



export default VideoCard;

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
                <div className="p-4 flex justify-center">
                    <button
                        onClick={onViewArticle}
                        className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-full shadow-md transition-colors duration-300"
                    >
                        View Article
                    </button>
                </div>

            </div>

        </div >
    );
};



export default VideoCard;

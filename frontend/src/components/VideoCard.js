import React from "react";

const VideoCard = ({ videoSrc, onViewArticle }) => {
    return (
        <div className="max-w-sm mx-auto my-4 bg-white border border-gray-200 rounded-lg shadow-lg overflow-hidden snap-center bg-gray-50 border border-gray-200 rounded-lg shadow-lg overflow-hidden">
            <video
                className="w-full h-auto"
                controls
                src={videoSrc}
                type="video/mp4"
            >
                Your browser does not support the video tag.
            </video>
            <div className="p-4 flex justify-center">
                <button
                    onClick={onViewArticle}
                    className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-full shadow-md transition-colors duration-300"
                >
                    View Article
                </button>
            </div>
        </div>
    );
};



export default VideoCard;

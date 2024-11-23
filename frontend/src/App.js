import React, { useState } from "react";
import VideoCard from "./components/VideoCard";
import ArticleModal from "./components/ArticleModal";

const App = () => {
    const [isArticleOpen, setArticleOpen] = useState(false);
    const [currentVideo, setCurrentVideo] = useState(null);

    const videoList = [
        { id: 1, src: "http://localhost:8005/output_0.mp4" },
        { id: 2, src: "http://localhost:8005/output_0.mp4" },
        { id: 3, src: "http://localhost:8005/output_0.mp4" },
    ];

    const handleViewArticle = (videoId) => {
        setCurrentVideo(videoId);
        setArticleOpen(true);
    };

    const handleCloseArticle = () => {
        setArticleOpen(false);
    };

    return (
        <div className="min-h-screen bg-gray-100">
            {!isArticleOpen && (
                <div
                    className="h-screen overflow-y-scroll snap-y snap-mandatory"
                    style={{ scrollBehavior: "smooth" }}
                >
                    {videoList.map((video) => (
                        <VideoCard
                            key={video.id}
                            videoSrc={video.src}
                            onViewArticle={() => handleViewArticle(video.id)}
                        />
                    ))}
                </div>
            )}
            <ArticleModal isOpen={isArticleOpen} onClose={handleCloseArticle} />
        </div>
    );
};

export default App;

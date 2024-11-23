import React from "react";

const ArticleModal = ({ isOpen, onClose, content }) => {
    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex">
            <div className="bg-white h-full w-full overflow-auto relative flex justify-center">
                <div className="w-7/12 my-24">
                    <button
                        onClick={onClose}
                        className="absolute top-4 right-4 bg-red-500 hover:bg-red-600 text-white font-bold py-1 px-3 rounded-full shadow-md"
                    >
                        ×
                    </button>
                    <div className="p-6">
                        <h1 className="text-2xl font-bold mb-4">{content.title}</h1>

                        {content.sections.map((section) => (<div>
                            <h2 className="text-xl font-bold mb-4">{section.title}</h2>
                            <p className="text-gray-700">{section.content}</p>
                        </div>))}


                    </div>
                </div>
            </div>
        </div>
    );
};

export default ArticleModal;

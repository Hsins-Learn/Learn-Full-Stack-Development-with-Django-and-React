import React from 'react';

const ImageHelper = ({ product }) => {
  const imageUrl = product ? product.image : 'https://i.imgur.com/z7EiIyZ.jpg';
  return (
    <div className="rounded border border-success p-2">
      <img
        src={imageUrl}
        style={{ maxHeight: '100%', maxWidth: '100%' }}
        className="mb-3 rounded"
        alt=""
      />
    </div>
  );
};

export default ImageHelper;

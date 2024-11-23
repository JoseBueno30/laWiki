import React from 'react';
import './wiki-edit-page.css';
import { Button } from "antd";

const WikiEditPage = () => {
  return (
      <section className='edit-wiki-section'>
        <div className='edit-wiki-container'>
          <h1>Edit Wiki Information</h1>

          <div className='edit-wiki-item'>
            <label htmlFor="edit-wiki-title" className="edit-wiki-label">Title</label>
            <input 
              type='text' 
              id="edit-wiki-title" 
              className='edit-wiki-text' 
            />
          </div>

          <div className='edit-wiki-item'>
            <label htmlFor="edit-wiki-description" className="edit-wiki-label">Description</label>
            <textarea 
              id="edit-wiki-description" 
              className='edit-wiki-textarea' 
            />
          </div>
          
          <div className='edit-wiki-item'>
            <label htmlFor="edit-wiki-tags" className="edit-wiki-label">Tags</label>
            <textarea 
              id="edit-wiki-tags" 
              className='edit-wiki-textarea' 
            />
          </div>

          <div className='edit-wiki-buttons-section'>
            <Button color='primary' variant='solid'>Save wiki</Button>
            <Button color='default' variant='outlined'>Cancel</Button>
            <Button color='danger' variant='outlined' className='right-button'>Delete wiki</Button>
          </div>
        </div>
      </section>
  );
};

export default WikiEditPage;

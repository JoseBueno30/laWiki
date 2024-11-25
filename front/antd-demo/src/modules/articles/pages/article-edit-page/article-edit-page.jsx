import React, { useState } from "react";
import { Tag, Input, Button } from "antd";
import { PlusOutlined } from "@ant-design/icons";
import './article-edit-page.css';

const ArticleEditPage = () => {
  const [tags, setTags] = useState(["Tag 1", "Tag 2", "Tag 3"]);
  const [newTag, setNewTag] = useState("");
  const [isInputVisible, setIsInputVisible] = useState(false);

  const addTag = () => {
    if (newTag.trim() && !tags.includes(newTag)) {
      setTags([...tags, newTag]);
      setNewTag("");
      setIsInputVisible(false);
    }
  };

  const removeTag = (tag) => {
    setTags(tags.filter((t) => t !== tag));
  };
  return (
    <section className="edit-article-section">
      <div className="edit-article-container">
        <h1>Edit Article Information</h1>

        <div className="edit-article-item">
          <label htmlFor="edit-article-title" className="edit-article-label">
            Title
          </label>
          <input type="text" id="edit-article-title" className="edit-article-text" />
        </div>

        <div className="edit-article-item">
          <label htmlFor="edit-article-description" className="edit-article-label">
            Description
          </label>
          <textarea
            id="edit-article-description"
            className="edit-article-textarea"
          />
        </div>

        <div className="edit-article-item">
          <label htmlFor="edit-article-tags" className="edit-article-label">
            Tags
          </label>
          <div className="tags-section edit-article-textarea">
            {tags.map((tag) => (
              <Tag
                key={tag}
                closable
                onClose={() => removeTag(tag)}
                className="tag-item"
              >
                {tag}
              </Tag>
            ))}

            {isInputVisible ? (
              <Input
                size="small"
                value={newTag}
                onChange={(e) => setNewTag(e.target.value)}
                onPressEnter={addTag}
                onBlur={addTag}
                placeholder="New Tag"
                className="tag-input"
              />
            ) : (
              <Button
                size="small"
                icon={<PlusOutlined />}
                onClick={() => setIsInputVisible(true)}
                className="add-tag-button"
              >
                New Tag
              </Button>
            )}
          </div>
        </div>

        <div className="edit-article-buttons-section">
          <Button type="primary">Save article</Button>
          <Button>Cancel</Button>
          <Button danger className="right-button">
            Delete article
          </Button>
        </div>
      </div>
    </section>
  );
};

export default ArticleEditPage;

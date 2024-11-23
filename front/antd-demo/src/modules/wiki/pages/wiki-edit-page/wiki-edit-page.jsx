import React, { useState } from "react";
import { Tag, Input, Button } from "antd";
import { PlusOutlined } from "@ant-design/icons";
import "./wiki-edit-page.css";

const WikiEditPage = () => {
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
    <section className="edit-wiki-section">
      <div className="edit-wiki-container">
        <h1>Edit Wiki Information</h1>

        <div className="edit-wiki-item">
          <label htmlFor="edit-wiki-title" className="edit-wiki-label">
            Title
          </label>
          <input type="text" id="edit-wiki-title" className="edit-wiki-text" />
        </div>

        <div className="edit-wiki-item">
          <label htmlFor="edit-wiki-description" className="edit-wiki-label">
            Description
          </label>
          <textarea
            id="edit-wiki-description"
            className="edit-wiki-textarea"
          />
        </div>

        <div className="edit-wiki-item">
          <label htmlFor="edit-wiki-tags" className="edit-wiki-label">
            Tags
          </label>
          <div className="tags-section edit-wiki-textarea">
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

        <div className="edit-wiki-buttons-section">
          <Button type="primary">Save wiki</Button>
          <Button>Cancel</Button>
          <Button danger className="right-button">
            Delete wiki
          </Button>
        </div>
      </div>
    </section>
  );
};

export default WikiEditPage;

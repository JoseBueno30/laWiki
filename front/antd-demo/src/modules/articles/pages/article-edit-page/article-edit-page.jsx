import React, { useState } from "react";
import { Tag, Select, Button } from "antd";
import { PlusOutlined } from "@ant-design/icons";
import './article-edit-page.css';

const { Option } = Select;

const ArticleEditPage = () => {
  const [tags, setTags] = useState(["Tag 1", "Tag 2", "Tag 3"]);
  const [availableTags, setAvailableTags] = useState([
    "Tag 1",
    "Tag 2",
    "Tag 3",
    "Tag 4",
    "Tag 5",
  ]);

  const addTag = (value) => {
    if (value && !tags.includes(value)) {
      setTags([...tags, value]);
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

            <Select
              placeholder="Select a tag"
              style={{ width: 200 }}
              onChange={addTag}
              className="tag-select"
            >
              {availableTags
                .filter((tag) => !tags.includes(tag))
                .map((tag) => (
                  <Option key={tag} value={tag}>
                    {tag}
                  </Option>
                ))}
            </Select>
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

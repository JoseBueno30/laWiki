import React, { useState } from "react";
import { Tag, Select, Button, Input, Upload } from "antd";
const { TextArea } = Input;
import { PlusOutlined, UploadOutlined } from "@ant-design/icons";
import './article-edit-page.css';
import MapComponent from "../MapComponent";

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

  const props = {
    name: 'file',
    action: 'https://660d2bd96ddfa2943b33731c.mockapi.io/api/upload',
    headers: {
      authorization: 'authorization-text',
    },
    onChange(info) {
      if (info.file.status !== 'uploading') {
        console.log(info.file, info.fileList);
      }
      if (info.file.status === 'done') {
        message.success(`${info.file.name} file uploaded successfully`);
      } else if (info.file.status === 'error') {
        message.error(`${info.file.name} file upload failed.`);
      }
    },
  };

  return (
    <section className="edit-article-section">
      <div className="edit-article-container">
        <h1>Edit Article Information</h1>

        <div className="edit-article-item">
          <label htmlFor="edit-article-title" className="edit-article-label">
            Title
          </label>
          <Input id="edit-article-title"></Input>
        </div>

        <div className="edit-article-item">
          <label htmlFor="edit-article-description" className="edit-article-label">
            Description
          </label>
            <TextArea
              id="edit-article-description" 
              autoSize={{ minRows: 6, maxRows: 10 }}
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
        
        <div className="edit-article-item">
          <h2>Selecciona una ubicación en el mapa:</h2>
          <MapComponent />
        </div>

        <div className="edit-article-item">
          <h2>Insertar una imagen:</h2>
          <Upload {...props}>
            <Button icon={<UploadOutlined />}>Click to Upload</Button>
          </Upload>
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

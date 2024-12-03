import React, { useState, useEffect } from "react";
import { Tag, Select, Button, Input, Upload, Modal, Flex } from "antd";
const { TextArea } = Input;
import { PlusOutlined, UploadOutlined } from "@ant-design/icons";
import "./article-edit-page.css";
import MapComponent from "../../components/map-component/MapComponent";
import MapConfigurator from "../../components/map-configurator/map-configurator";
import MapView from "../../components/map-view/map-view";
import ReactDOM from "react-dom/client";
import JsxParser from "react-jsx-parser";
import { uploadImage } from "../../service/article_service";

const { Option } = Select;



const ArticleEditPage = () => {
  const [body, setBody] = useState("");
  const [tags, setTags] = useState(["Tag 1", "Tag 2", "Tag 3"]);
  const [availableTags, setAvailableTags] = useState([
    "Tag 1",
    "Tag 2",
    "Tag 3",
    "Tag 4",
    "Tag 5",
  ]);
  const [images, setImages] = useState([]); // Estado para almacenar imágenes seleccionadas

  const [isModalOpen, setIsModalOpen] = useState(false);
  const showModal = () => {
    setIsModalOpen(true);
  };

  const addTag = (value) => {
    if (value && !tags.includes(value)) {
      setTags([...tags, value]);
    }
  };

  const removeTag = (tag) => {
    setTags(tags.filter((t) => t !== tag));
  };

  const customRequest = async ({ file, onSuccess, onError }) => {
    try {
      const imageUrl = await uploadImage(file);

      const wikiTextImage = `[[File:${imageUrl}|title=""]]`;
      
      setBody(`${body}\n${wikiTextImage}`);

      onSuccess();
    } catch (error) {
      console.error('Error uploading file:', error);
      onError(error);
    }
  };

  const handleCancel = () => setIsModalOpen(false);

  const onMapSave = (wikiTextTag) => {
    setBody(`${body}\n${wikiTextTag}`);
    setIsModalOpen(false);
  };

  return (
    <section className="edit-article-section">
      <div className="edit-article-container">
        <h1>Edit Article Information</h1>

        <div className="edit-article-item">
          <label htmlFor="edit-article-title" className="edit-article-label">
            Title
          </label>
          <Input id="edit-article-title" />
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

        <Flex align="center" justify="space-evenly" style={{ width: "100%" }}>
          <div>
            <Button type="primary" onClick={showModal}>
              Insertar mapa
            </Button>
            <Modal
              title="Configuración del Mapa"
              open={isModalOpen} // Aquí podrías guardar el mapa cuando se pulse OK
              width="80vw" // Ancho personalizado para adaptarse mejor al mapa
              style={{ height: "70vh", overflow: "hidden" }} // Altura ajustada
              onCancel={handleCancel}
              destroyOnClose
            >
              <MapConfigurator onSave={onMapSave} />
            </Modal>
          </div>

          <div>
            <Upload
              customRequest={customRequest}
              multiple={false}
              showUploadList={false}
              accept="image/*"
            >
              <Button icon={<UploadOutlined />}>Insertar imagen</Button>
            </Upload>
          </div>
        </Flex>

        {/* Vista previa de imágenes */}
        <div className="image-preview-container" style={{ marginTop: "20px" }}>
          {images.map((image, index) => (
            <div
              key={index}
              className="image-preview"
              style={{ marginBottom: "10px" }}
            >
              <img
                src={image}
                alt={`Preview ${index}`}
                style={{
                  maxWidth: "100%",
                  height: "auto",
                  borderRadius: "8px",
                  border: "1px solid #ddd",
                }}
              />
            </div>
          ))}
        </div>

        <div className="edit-article-item">
          <label
            htmlFor="edit-article-description"
            className="edit-article-label"
          >
            Body
          </label>
          <TextArea
            id="edit-article-description"
            value={body} // El valor del textarea es el estado
            onChange={(e) => {
              setBody(e.target.value), console.log(body);
            }}
            autoSize={{ minRows: 6, maxRows: 30 }}
          />
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

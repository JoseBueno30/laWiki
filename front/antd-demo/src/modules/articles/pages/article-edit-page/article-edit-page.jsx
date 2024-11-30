import React, { useState } from "react";
import { Tag, Select, Button, Input, Upload } from "antd";
const { TextArea } = Input;
import { PlusOutlined, UploadOutlined } from "@ant-design/icons";
import "./article-edit-page.css";
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
  const [maps, setMaps] = useState([]);
  const [images, setImages] = useState([]); // Estado para almacenar imágenes seleccionadas

  const addTag = (value) => {
    if (value && !tags.includes(value)) {
      setTags([...tags, value]);
    }
  };

  const removeTag = (tag) => {
    setTags(tags.filter((t) => t !== tag));
  };

  const addMap = () => {
    setMaps((prevMaps) => [
      ...prevMaps,
      <MapComponent key={prevMaps.length} />,
    ]);
  };

  // Manejar la selección de imágenes
  const handleImageUpload = (file) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      setImages((prevImages) => [...prevImages, e.target.result]); // Agregar la imagen al estado
    };
    reader.readAsDataURL(file); // Convertir archivo en base64
    return false; // Evitar la carga automática de archivos por el componente Upload
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

        <div className="edit-article-item">
          <label htmlFor="edit-article-description" className="edit-article-label">
            Body
          </label>
          <TextArea
            id="edit-article-description"
            autoSize={{ minRows: 6, maxRows: 10 }}
          />
        </div>

        <div className="edit-article-item">
          <h2>Selecciona una ubicación en el mapa:</h2>
          {maps}
          <Button
            type="dashed"
            icon={<PlusOutlined />}
            onClick={addMap}
            style={{ marginTop: "10px" }}
          >
            Agregar mapa
          </Button>
        </div>

        <div className="edit-article-item">
          <h2>Insertar una imagen:</h2>
          <Upload
            beforeUpload={handleImageUpload} // Maneja la imagen antes de la carga
            multiple={true} // Permitir múltiples imágenes
            showUploadList={false} // Ocultar la lista predeterminada de Ant Design
          >
            <Button icon={<UploadOutlined />}>Seleccionar imagen</Button>
          </Upload>

          {/* Vista previa de imágenes */}
          <div className="image-preview-container" style={{ marginTop: "20px" }}>
            {images.map((image, index) => (
              <div key={index} className="image-preview" style={{ marginBottom: "10px" }}>
                <img
                  src={image}
                  alt={`Preview ${index}`}
                  style={{ maxWidth: "100%", height: "auto", borderRadius: "8px", border: "1px solid #ddd" }}
                />
              </div>
            ))}
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

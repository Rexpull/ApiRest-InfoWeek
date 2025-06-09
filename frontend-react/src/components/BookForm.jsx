import { useState, useEffect } from 'react';

export default function BookForm({ book, onSubmit, onCancel, title }) {
  const [formData, setFormData] = useState({
    titulo: '',
    autor: '',
    ano: '',
    genero: '',
    isbn: '',
    paginas: '',
    descricao: ''
  });

  useEffect(() => {
    if (book) {
      setFormData({
        titulo: book.titulo || '',
        autor: book.autor || '',
        ano: book.ano || '',
        genero: book.genero || '',
        isbn: book.isbn || '',
        paginas: book.paginas || '',
        descricao: book.descricao || ''
      });
    }
  }, [book]);

  const handleSubmit = (e) => {
    e.preventDefault();
    
    const submitData = {
      ...formData,
      ano: formData.ano ? parseInt(formData.ano) : undefined,
      paginas: formData.paginas ? parseInt(formData.paginas) : undefined
    };

    // Remove campos vazios
    Object.keys(submitData).forEach(key => {
      if (submitData[key] === '' || submitData[key] === undefined) {
        delete submitData[key];
      }
    });

    onSubmit(submitData);
  };

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4 z-50">
      <div className="card w-full max-w-2xl max-h-[90vh] overflow-y-auto">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold text-gray-800">{title}</h2>
          <button
            onClick={onCancel}
            className="text-gray-500 hover:text-gray-700 text-2xl"
          >
            ×
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Título *
              </label>
              <input
                type="text"
                name="titulo"
                value={formData.titulo}
                onChange={handleInputChange}
                className="input-field"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Autor *
              </label>
              <input
                type="text"
                name="autor"
                value={formData.autor}
                onChange={handleInputChange}
                className="input-field"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Ano
              </label>
              <input
                type="number"
                name="ano"
                value={formData.ano}
                onChange={handleInputChange}
                className="input-field"
                min="1000"
                max="2030"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Gênero
              </label>
              <input
                type="text"
                name="genero"
                value={formData.genero}
                onChange={handleInputChange}
                className="input-field"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                ISBN
              </label>
              <input
                type="text"
                name="isbn"
                value={formData.isbn}
                onChange={handleInputChange}
                className="input-field"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Páginas
              </label>
              <input
                type="number"
                name="paginas"
                value={formData.paginas}
                onChange={handleInputChange}
                className="input-field"
                min="1"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Descrição
            </label>
            <textarea
              name="descricao"
              value={formData.descricao}
              onChange={handleInputChange}
              className="input-field"
              rows="3"
            />
          </div>

          <div className="flex gap-4 justify-end pt-4">
            <button
              type="button"
              onClick={onCancel}
              className="btn-secondary"
            >
              Cancelar
            </button>
            <button
              type="submit"
              className="btn-primary"
            >
              {book ? 'Salvar' : 'Adicionar'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
} 
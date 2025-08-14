function Asistente() {
    this.section = "sectionIA";    
    this.titulo = "#saludoIA p";
    this.conversacion = "chat-container"; 
        
}

Asistente.prototype.iniciar = function() {
    
    const elemento = document.getElementById(this.section);
    if (!elemento) return console.error("No se encontró bloque");

    if (elemento.dataset.estado !== "enlinea") {
        elemento.dataset.estado = "enlinea";
        document.querySelector(this.titulo).textContent = "Asistente virtual";
    }
              
    
};





Asistente.prototype.enviar = function(mensajeUsuario) {
    if (!mensajeUsuario.trim()) return;

    // Mostrar mensaje del usuario
    this.agregarMensaje("user", mensajeUsuario);


    // Consultar a la IA
    this.consultarIA(mensajeUsuario);
    
        
};




Asistente.prototype.agregarMensaje = function(tipo, texto) {
    const fila = document.createElement("div");
    fila.className = tipo === "user"
        ? "d-flex justify-content-end mb-2"
        : "d-flex justify-content-start mb-2";

    const burbuja = document.createElement("div");
    burbuja.className = "chat-bubble " + tipo + " mx-3 shadow-3-strong";

    if (tipo === "user") {
        const lineas = texto.split("\n");
        lineas.forEach(function(linea, index) {
            const p = document.createElement("p");
            p.className = index === lineas.length - 1 ? "mb-0" : "mb-1";
            p.textContent = linea.trim();
            burbuja.appendChild(p);
        });
    } else {
        // respuesta del servidor: puede tener HTML o formateo más compacto
       
         burbuja.innerHTML = this.markdownToHTML(texto);
    }

    fila.appendChild(burbuja);

    const contenedor = document.getElementById(this.conversacion);
    contenedor.appendChild(fila);
    contenedor.scrollTop = contenedor.scrollHeight;
};




Asistente.prototype.consultarIA = function(prompt) {
    const self = this;
    
      console.log("Enviando a API:", { prompt: prompt });

    
    
    // Mostrar animación de espera (ya se auto-inserta)
    const waitingMessage = this.mostrarAnimacionEspera();

    // const baseURL = window.location.origin;
    const baseURL = "http://localhost:8070";

    

    fetch(baseURL + "/orasifen/api/genia/rag", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: prompt })
    })
    .then(response => response.json())
    .then(data => {
        // Eliminar mensaje de espera antes de mostrar respuesta
        waitingMessage.remove();
        //const formattedText = this.markdownToHTML(data.response_text);
        //self.agregarMensaje("assistant", formattedText);
        self.agregarMensaje("assistant", data.response);
        
        console.log(data.response);
    })
    .catch(error => {
        console.error("Error:", error);
        // Eliminar mensaje de espera antes de mostrar error
        waitingMessage.remove();
        self.agregarMensaje("assistant", "Ocurrió un error al contactar la IA.");
    })
    .finally(() => {
        let btnChatIA = document.getElementById('btnChatIA');
        btnChatIA.disabled = false;
    });
    
};




Asistente.prototype.mostrarAnimacionEspera = function() {
    const typing = document.createElement('div');
    typing.className = 'd-flex justify-content-start mb-2 message-animation';
    
    typing.innerHTML = `
      <div class="p-3 d-flex align-items-center">
        <div class="typing-indicator"> <!-- Esto seguiría siendo custom -->
          <div class="typing-dot"></div>
          <div class="typing-dot"></div>
          <div class="typing-dot"></div>
        </div>
      </div>
    `;    
    
    // Insertar directamente en el contenedor
    const chat = document.getElementById(this.conversacion);
    chat.appendChild(typing);
    
    // Scroll automático al mensaje nuevo
    typing.scrollIntoView({ 
        behavior: 'smooth',
        block: 'nearest'
    });    
    
    
    return typing;
};




Asistente.prototype.markdownToHTML2 = function(text) {
  let html = text
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')      // bold
    .replace(/\*(.*?)\*/g, '<em>$1</em>')                  // italic
    .replace(/^[*-] (.*)$/gm, '<li>$1</li>')                // list item
    .replace(/(<li>[\s\S]*?<\/li>)/g, '<ul>$1</ul>')        // wrap with <ul>
    .replace(/\n{2,}/g, '</p><p>')                          // double line break = new paragraph
    .replace(/\n/g, '<br>');                                // single line break

    // Eliminaciones específicas
    html = html.replace(/<p>\s*<\/p>/g, '');
    html = html.replace(/<br\s*\/?>/g, '');

    // boostrap 
    html = html.replace(/<p>/g, '<p class="mb-1">');
    html = html.replace(/<ul>/g, '<ul class="mb-1">');


  return html;
};


Asistente.prototype.markdownToHTML = function(text) {
  let html = text
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')     // **bold**
    .replace(/\*(.*?)\*/g, '<em>$1</em>')                 // *italic*
    .replace(/^\s*[-*] (.*)$/gm, '<li>$1</li>')           // - list item

    // Agrupar <li> consecutivos dentro de un <ul>
    .replace(/(<li>.*<\/li>\s*)+/g, match => {
      const items = match.trim().replace(/\s*<\/li>\s*/g, '</li>');
      return `<ul class="mb-1">${items}</ul>`;
    })

    .replace(/\n{2,}/g, '</p><p class="mb-1">')           // párrafos
    .replace(/\n/g, '<br>');                              // saltos de línea

  // Asegurar que el contenido esté dentro de <p>
  if (!/^<p/.test(html)) {
    html = `<p class="mb-1">${html}</p>`;
  }

  return html;
};

// Simplified audio embed for local MP3 files
document.addEventListener('DOMContentLoaded', function() {
  // Find all audio links
  const audioLinks = document.querySelectorAll('a[href$=".mp3"]');
  
  audioLinks.forEach(function(link) {
    // Get the audio file path
    const audioSrc = link.getAttribute('href');
    
    // Create audio player
    const audioPlayer = document.createElement('audio');
    audioPlayer.controls = true;
    audioPlayer.preload = 'metadata';
    audioPlayer.style.width = '100%';
    audioPlayer.style.maxWidth = '500px';
    
    // Create source element
    const source = document.createElement('source');
    source.src = audioSrc;
    source.type = 'audio/mpeg';
    
    audioPlayer.appendChild(source);
    
    // Add fallback text
    const fallback = document.createTextNode('Your browser does not support the audio element. ');
    const downloadLink = document.createElement('a');
    downloadLink.href = audioSrc;
    downloadLink.textContent = 'Download audio';
    
    audioPlayer.appendChild(fallback);
    audioPlayer.appendChild(downloadLink);
    
    // Replace the link with the audio player
    link.parentNode.replaceChild(audioPlayer, link);
  });
});

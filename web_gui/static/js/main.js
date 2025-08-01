// MCI Papers Database - Custom JavaScript

document.addEventListener('DOMContentLoaded', function() {
    console.log('MCI Papers Web GUI loaded');
    
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            var alertInstance = new bootstrap.Alert(alert);
            alertInstance.close();
        });
    }, 5000);
    
    // Search functionality
    initializeSearch();
    
    // Language toggle
    initializeLanguageToggle();
    
    // Filter functionality
    initializeFilters();
    
    // File upload handling
    initializeFileUpload();
});

function initializeSearch() {
    const searchInput = document.querySelector('input[name="search"]');
    const searchForm = document.querySelector('form[role="search"]');
    
    if (searchInput && searchForm) {
        let searchTimeout;
        
        // Real-time search (debounced)
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            
            searchTimeout = setTimeout(function() {
                const query = searchInput.value.trim();
                if (query.length > 2) {
                    performAjaxSearch(query);
                } else {
                    hideSearchResults();
                }
            }, 300);
        });
        
        // Show search results dropdown
        searchInput.addEventListener('focus', function() {
            const query = searchInput.value.trim();
            if (query.length > 2) {
                performAjaxSearch(query);
            }
        });
        
        // Hide search results when clicking outside
        document.addEventListener('click', function(e) {
            if (!searchForm.contains(e.target)) {
                hideSearchResults();
            }
        });
    }
}

function performAjaxSearch(query) {
    const language = getLanguageFromUrl();
    
    fetch(`/api/search?q=${encodeURIComponent(query)}&lang=${language}`)
        .then(response => response.json())
        .then(data => {
            showSearchResults(data.results);
        })
        .catch(error => {
            console.error('Search error:', error);
        });
}

function showSearchResults(results) {
    // Remove existing dropdown
    hideSearchResults();
    
    const searchForm = document.querySelector('form[role="search"]');
    const dropdown = document.createElement('div');
    dropdown.className = 'search-results-dropdown position-absolute bg-white border rounded shadow-lg mt-1';
    dropdown.style.cssText = 'top: 100%; left: 0; right: 0; z-index: 1050; max-height: 300px; overflow-y: auto;';
    
    if (results.length === 0) {
        dropdown.innerHTML = '<div class="p-3 text-muted">검색 결과가 없습니다.</div>';
    } else {
        const resultHtml = results.map(paper => `
            <a href="/paper/${paper.id}" class="d-block p-2 text-decoration-none border-bottom">
                <div class="fw-semibold text-dark">${paper.title}</div>
                <small class="text-muted">${paper.journal} (${paper.year}) - PMID: ${paper.pmid}</small>
            </a>
        `).join('');
        dropdown.innerHTML = resultHtml;
    }
    
    searchForm.style.position = 'relative';
    searchForm.appendChild(dropdown);
}

function hideSearchResults() {
    const existing = document.querySelector('.search-results-dropdown');
    if (existing) {
        existing.remove();
    }
}

function getLanguageFromUrl() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('lang') || 'korean';
}

function initializeLanguageToggle() {
    // Update language links to preserve current URL parameters
    const languageLinks = document.querySelectorAll('.dropdown-menu a[href*="lang="]');
    
    languageLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const url = new URL(window.location);
            const targetLang = this.href.includes('lang=korean') ? 'korean' : 'english';
            
            url.searchParams.set('lang', targetLang);
            window.location.href = url.toString();
        });
    });
}

function initializeFilters() {
    const filterForm = document.getElementById('filter-form');
    if (filterForm) {
        const filterInputs = filterForm.querySelectorAll('select, input');
        
        filterInputs.forEach(input => {
            input.addEventListener('change', function() {
                // Auto-submit form when filter changes
                setTimeout(() => filterForm.submit(), 100);
            });
        });
    }
    
    // Clear filters button
    const clearFiltersBtn = document.getElementById('clear-filters');
    if (clearFiltersBtn) {
        clearFiltersBtn.addEventListener('click', function(e) {
            e.preventDefault();
            
            const url = new URL(window.location);
            const language = url.searchParams.get('lang') || 'korean';
            
            // Keep only the language parameter
            const newUrl = new URL(window.location.pathname, window.location.origin);
            newUrl.searchParams.set('lang', language);
            
            window.location.href = newUrl.toString();
        });
    }
}

function initializeFileUpload() {
    const fileInput = document.querySelector('input[type="file"][accept=".csv"]');
    const uploadForm = document.getElementById('import-form');
    
    if (fileInput && uploadForm) {
        fileInput.addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                // Validate file type
                if (!file.name.toLowerCase().endsWith('.csv')) {
                    alert('CSV 파일만 업로드 가능합니다.');
                    this.value = '';
                    return;
                }
                
                // Validate file size (max 16MB)
                if (file.size > 16 * 1024 * 1024) {
                    alert('파일 크기가 너무 큽니다. 16MB 이하의 파일을 선택해주세요.');
                    this.value = '';
                    return;
                }
                
                // Show file info
                updateFileInfo(file);
            }
        });
        
        // Drag and drop functionality
        const uploadArea = document.querySelector('.upload-area');
        if (uploadArea) {
            uploadArea.addEventListener('dragover', function(e) {
                e.preventDefault();
                this.classList.add('drag-over');
            });
            
            uploadArea.addEventListener('dragleave', function(e) {
                e.preventDefault();
                this.classList.remove('drag-over');
            });
            
            uploadArea.addEventListener('drop', function(e) {
                e.preventDefault();
                this.classList.remove('drag-over');
                
                const files = e.dataTransfer.files;
                if (files.length > 0) {
                    fileInput.files = files;
                    fileInput.dispatchEvent(new Event('change'));
                }
            });
        }
    }
}

function updateFileInfo(file) {
    const fileInfo = document.getElementById('file-info');
    if (fileInfo) {
        const fileSize = (file.size / 1024).toFixed(1);
        fileInfo.innerHTML = `
            <div class="alert alert-info">
                <i class="bi bi-file-earmark-text"></i>
                선택된 파일: <strong>${file.name}</strong> (${fileSize} KB)
            </div>
        `;
    }
}

// Utility functions
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('ko-KR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

function formatNumber(num) {
    return num.toLocaleString('ko-KR');
}

function showLoading(element) {
    if (element) {
        element.innerHTML = `
            <div class="spinner-container">
                <div class="custom-spinner"></div>
            </div>
        `;
    }
}

function hideLoading() {
    const spinners = document.querySelectorAll('.spinner-container');
    spinners.forEach(spinner => spinner.remove());
}

// Export functions for global use
window.MCIPapers = {
    showLoading,
    hideLoading,
    formatDate,
    formatNumber,
    performAjaxSearch,
    getLanguageFromUrl
};

// Handle page visibility for real-time updates
document.addEventListener('visibilitychange', function() {
    if (!document.hidden) {
        // Page became visible, refresh data if needed
        console.log('Page visible, checking for updates...');
    }
});

// Handle online/offline status
window.addEventListener('online', function() {
    console.log('Connection restored');
    // Show notification or refresh data
});

window.addEventListener('offline', function() {
    console.log('Connection lost');
    // Show offline notification
});

// Service Worker registration (for future PWA features)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        // navigator.serviceWorker.register('/sw.js')
        //     .then(function(registration) {
        //         console.log('SW registered: ', registration);
        //     })
        //     .catch(function(registrationError) {
        //         console.log('SW registration failed: ', registrationError);
        //     });
    });
}

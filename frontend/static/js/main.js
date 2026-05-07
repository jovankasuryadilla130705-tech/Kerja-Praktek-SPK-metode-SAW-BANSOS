/**
 * ==========================================================================
 *  main.js — JavaScript Utama Sistem Klasifikasi Bansos
 * ==========================================================================
 *  File ini berisi seluruh logika JavaScript frontend untuk aplikasi,
 *  termasuk:
 *    1. Toggle Sidebar (navigasi responsif mobile)
 *    2. Tab Switcher (berpindah antara Input Manual & Import Massal)
 *    3. Inisialisasi Chart.js (Pie Chart & Bar Chart di Dashboard)
 *    4. Drag & Drop File Upload
 *
 *  File ini dimuat di semua halaman melalui tag <script> di template HTML.
 *  Fungsi yang tidak relevan di halaman tertentu akan di-skip secara
 *  otomatis melalui pengecekan keberadaan elemen DOM.
 * ==========================================================================
 */


// ==========================================================================
//  1. SIDEBAR TOGGLE — Navigasi Responsif untuk Mobile
// ==========================================================================
// Pada layar kecil (< lg / 1024px), sidebar disembunyikan secara default
// dan ditampilkan saat pengguna menekan tombol hamburger.
// Overlay gelap ditampilkan di belakang sidebar saat terbuka.

function toggleSidebar() {
    var sidebar = document.getElementById('sidebar');
    var overlay = document.getElementById('sidebar-overlay');

    if (sidebar && overlay) {
        if (sidebar.classList.contains('-translate-x-full')) {
            // Buka sidebar — geser masuk dari kiri
            sidebar.classList.remove('-translate-x-full');
            overlay.classList.remove('hidden');
            setTimeout(function() { overlay.classList.remove('opacity-0'); }, 10);
        } else {
            // Tutup sidebar — geser keluar ke kiri
            sidebar.classList.add('-translate-x-full');
            overlay.classList.add('opacity-0');
            setTimeout(function() { overlay.classList.add('hidden'); }, 300);
        }
    }
}


// ==========================================================================
//  1B. PROFILE DROPDOWN TOGGLE
// ==========================================================================
function toggleProfileDropdown(event) {
    if (event) {
        event.stopPropagation();
    }
    var menu = document.getElementById('profile-dropdown-menu');
    if (menu) {
        menu.classList.toggle('hidden');
    }
}

// Tutup dropdown jika klik di luar
document.addEventListener('click', function(event) {
    var menu = document.getElementById('profile-dropdown-menu');
    var container = document.getElementById('profile-dropdown-container');
    if (menu && !menu.classList.contains('hidden') && container) {
        if (!container.contains(event.target)) {
            menu.classList.add('hidden');
        }
    }
});


// ==========================================================================
//  2. TAB SWITCHER — Berpindah Tab di Halaman Klasifikasi
// ==========================================================================
// Halaman Klasifikasi memiliki 2 tab: "Input Manual" dan "Import Massal".
// Fungsi ini menyembunyikan konten tab yang tidak aktif dan menampilkan
// konten tab yang dipilih dengan efek visual (underline biru pada tab aktif).

function switchTab(tabId) {
    // Daftar ID tab yang tersedia.
    var tabs = ['manual', 'import'];

    // Nonaktifkan semua tab terlebih dahulu.
    tabs.forEach(function(t) {
        var tabElement = document.getElementById('tab-' + t);
        var contentElement = document.getElementById('content-' + t);
        if (tabElement && contentElement) {
            tabElement.classList.remove('tab-active', 'text-blue-600');
            tabElement.classList.add('text-gray-500');
            contentElement.classList.add('hidden');
        }
    });

    // Aktifkan tab yang dipilih.
    var activeTab = document.getElementById('tab-' + tabId);
    var activeContent = document.getElementById('content-' + tabId);

    if (activeTab && activeContent) {
        activeTab.classList.add('tab-active', 'text-blue-600');
        activeTab.classList.remove('text-gray-500');
        activeContent.classList.remove('hidden');
    }
}


// ==========================================================================
//  3. INISIALISASI CHART.JS — Grafik di Halaman Dashboard
// ==========================================================================
// Chart.js digunakan untuk menampilkan 2 grafik di Dashboard:
//   a. Pie/Doughnut Chart — Distribusi kelayakan (Layak vs Tidak Layak)
//   b. Bar Chart — Jumlah warga terklasifikasi per kelurahan
//
// Data grafik diambil dari variabel global `window.*` yang diisi oleh
// template Jinja2 di dashboard.html (dari backend Flask).

document.addEventListener('DOMContentLoaded', function() {

    // ------------------------------------------------------------------
    //  3a. PIE CHART (Doughnut) — Distribusi Kelayakan
    // ------------------------------------------------------------------
    // Menampilkan perbandingan jumlah warga Layak (hijau) vs Tidak Layak (merah).
    // Data diambil dari window.layakData dan window.tidakLayakData.
    var pieCanvas = document.getElementById('pieChart');

    if (pieCanvas) {
        new Chart(pieCanvas, {
            type: 'doughnut',
            data: {
                labels: ['Layak', 'Tidak Layak'],
                datasets: [{
                    data: [
                        window.layakData !== undefined ? window.layakData : 0,
                        window.tidakLayakData !== undefined ? window.tidakLayakData : 0
                    ],
                    backgroundColor: ['#10B981', '#EF4444'],  // Emerald-500, Red-500
                    borderWidth: 0,
                    hoverOffset: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            usePointStyle: true,
                            padding: 20,
                            font: { family: 'Inter', size: 12 }
                        }
                    }
                },
                cutout: '75%'  // Ukuran lubang tengah doughnut
            }
        });
    }

    // ------------------------------------------------------------------
    //  3b. BAR CHART — Perbandingan per Kelurahan
    // ------------------------------------------------------------------
    // Menampilkan jumlah warga terklasifikasi di setiap kelurahan.
    // Data diambil dari window.barLabels (nama kelurahan) dan
    // window.barData (jumlah warga).
    var barCanvas = document.getElementById('barChart');

    if (barCanvas) {
        new Chart(barCanvas, {
            type: 'bar',
            data: {
                // Gunakan data dari backend. Jika tidak ada, tampilkan kosong.
                labels: window.barLabels || [],
                datasets: [{
                    label: 'Total Terklasifikasi',
                    data: window.barData || [],
                    backgroundColor: '#3B82F6',  // Blue-500
                    borderRadius: 6,
                    barPercentage: 0.6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: { borderDash: [4, 4], color: '#e2e8f0' },
                        ticks: { font: { family: 'Inter' } }
                    },
                    x: {
                        grid: { display: false },
                        ticks: { font: { family: 'Inter' } }
                    }
                },
                plugins: {
                    legend: { display: false }
                }
            }
        });
    }


    // ==================================================================
    //  4. DRAG & DROP FILE UPLOAD — Area Upload di Import Massal
    // ==================================================================
    // Memungkinkan pengguna menarik (drag) file ke area upload atau
    // mengklik untuk memilih file. Nama file yang dipilih ditampilkan.

    var dropZone = document.getElementById('dropZone');
    var fileInput = document.getElementById('file-upload');
    var fileNameDisplay = document.getElementById('file-name');

    if (dropZone && fileInput) {

        // Saat file di-drag memasuki area upload — beri highlight biru.
        dropZone.addEventListener('dragover', function(e) {
            e.preventDefault();
            dropZone.classList.add('border-blue-500', 'bg-blue-50');
        });

        // Saat file di-drag keluar dari area upload — hapus highlight.
        dropZone.addEventListener('dragleave', function() {
            dropZone.classList.remove('border-blue-500', 'bg-blue-50');
        });

        // Saat file di-drop ke area upload — masukkan ke input file.
        dropZone.addEventListener('drop', function(e) {
            e.preventDefault();
            dropZone.classList.remove('border-blue-500', 'bg-blue-50');

            if (e.dataTransfer.files.length) {
                fileInput.files = e.dataTransfer.files;
                updateFileName(e.dataTransfer.files[0].name);
            }
        });

        // Saat file dipilih melalui dialog — tampilkan nama file.
        fileInput.addEventListener('change', function() {
            if (fileInput.files.length) {
                updateFileName(fileInput.files[0].name);
            }
        });

        /**
         * Menampilkan nama file yang dipilih di bawah area upload.
         * @param {string} name - Nama file yang dipilih/didrop.
         */
        function updateFileName(name) {
            if (fileNameDisplay) {
                fileNameDisplay.textContent = 'File terpilih: ' + name;
                fileNameDisplay.classList.remove('hidden');
            }
        }
    }


    // ==================================================================
    //  5. FETCH & RENDER HISTORY (AJAX)
    // ==================================================================
    
    var historyTableBody = document.getElementById('history-table-body');
    var filterButtons = document.querySelectorAll('.filter-btn');
    
    if (historyTableBody && filterButtons.length > 0) {
        
        var currentKelurahan = 'all';
        var currentSearch = '';
        
        // Fungsi untuk mengambil dan merender data histori
        function fetchHistory(kelurahan, searchQuery = '') {
            historyTableBody.innerHTML = '<tr><td colspan="8" class="text-center py-8 text-gray-500">Memuat data...</td></tr>';
            
            var url = '/api/history';
            var params = [];
            if (kelurahan && kelurahan !== 'all') {
                params.push('kelurahan=' + encodeURIComponent(kelurahan));
            }
            if (searchQuery) {
                params.push('search=' + encodeURIComponent(searchQuery));
            }
            if (params.length > 0) {
                url += '?' + params.join('&');
            }
            
            fetch(url)
                .then(function(response) {
                    if (!response.ok) throw new Error('Network response was not ok');
                    return response.json();
                })
                .then(function(data) {
                    renderTable(data);
                })
                .catch(function(error) {
                    console.error('Error fetching history:', error);
                    historyTableBody.innerHTML = '<tr><td colspan="8" class="text-center py-8 text-red-500">Gagal memuat data histori.</td></tr>';
                });
        }
        
        function renderTable(data) {
            historyTableBody.innerHTML = '';
            
            if (data.length === 0) {
                var emptyMsg = currentSearch
                    ? 'Tidak ada data yang cocok dengan pencarian <b>"' + currentSearch + '"</b>.'
                    : (currentKelurahan !== 'all'
                        ? 'Belum ada data untuk kelurahan <b>' + currentKelurahan + '</b>.'
                        : 'Belum ada data klasifikasi yang tersimpan.');
                historyTableBody.innerHTML = `
                    <tr>
                        <td colspan="8" class="text-center py-16 px-4">
                            <div class="flex flex-col items-center gap-3 text-gray-400">
                                <i class="ph ph-magnifying-glass text-5xl opacity-40"></i>
                                <p class="text-sm font-medium text-gray-500">${emptyMsg}</p>
                                ${currentSearch || currentKelurahan !== 'all'
                                    ? '<p class="text-xs text-gray-400">Coba ubah kata kunci atau pilih kelurahan lain.</p>'
                                    : '<p class="text-xs text-gray-400">Gunakan menu <b>Klasifikasi Data</b> untuk menambahkan data warga.</p>'
                                }
                            </div>
                        </td>
                    </tr>`;
                return;
            }
            
            data.forEach(function(record, index) {
                var rank = index + 1;
                var nikFormatted = record.nik.toString().padStart(16, '0');
                
                var statusHtml = '';
                if (record.hasil_klasifikasi === "Layak") {
                    statusHtml = `<span class="inline-flex items-center gap-1 bg-emerald-100 text-emerald-700 px-2 sm:px-3 py-1 rounded-full text-[10px] sm:text-xs font-bold border border-emerald-200 whitespace-nowrap overflow-hidden"><i class="ph ph-check-circle text-sm"></i> Layak</span>`;
                } else {
                    statusHtml = `<span class="inline-flex items-center gap-1 bg-red-100 text-red-700 px-2 sm:px-3 py-1 rounded-full text-[10px] sm:text-xs font-bold border border-red-200 whitespace-nowrap overflow-hidden"><i class="ph ph-x-circle text-sm"></i> Tidak Layak</span>`;
                }
                
                var alasanHtml = record.alasan ? record.alasan : '-';
                var editUrl = '/edit/' + record.id;
                var deleteUrl = '/delete/' + record.id;
                
                var dateStr = record.created_at ? record.created_at.split(' ').slice(0, 3).join(' ') : '-';
                var timeStr = record.created_at_time ? record.created_at_time + ' WIB' : '';
                
                var tr = document.createElement('tr');
                tr.className = 'hover:bg-slate-50 transition-colors';
                
                tr.innerHTML = `
                    <td class="py-3 sm:py-4 px-4 sm:px-6 text-center font-bold text-gray-900">${rank}</td>
                    <td class="py-3 sm:py-4 px-4 sm:px-6 whitespace-nowrap">
                        <span class="text-xs sm:text-sm font-medium">${dateStr}</span>
                        <br><span class="text-[10px] sm:text-xs text-gray-400">${timeStr}</span>
                    </td>
                    <td class="py-3 sm:py-4 px-4 sm:px-6">
                        <div class="flex flex-col">
                            <span class="font-bold text-sm sm:text-base text-gray-900">${record.nama}</span>
                            <span class="text-[10px] sm:text-xs text-gray-500 font-mono">${nikFormatted}</span>
                        </div>
                    </td>
                    <td class="py-3 sm:py-4 px-4 sm:px-6">
                        <span class="text-xs sm:text-sm border border-gray-200 bg-gray-50 px-2 sm:px-3 py-1 rounded-full whitespace-nowrap">${record.kelurahan}</span>
                    </td>
                    <td class="py-3 sm:py-4 px-4 sm:px-6">
                        <div class="grid grid-cols-2 gap-x-2 gap-y-1">
                            ${record.detail_html}
                        </div>
                    </td>
                    <td class="py-3 sm:py-4 px-4 sm:px-6 text-center">
                        <div class="mb-1 text-xs font-bold text-blue-600">Skor: ${record.skor_saw ? record.skor_saw.toFixed(2) : '0.00'}</div>
                        ${statusHtml}
                    </td>
                    <td class="py-3 sm:py-4 px-4 sm:px-6 text-xs sm:text-sm text-gray-600 max-w-xs break-words">
                        ${alasanHtml}
                    </td>
                    <td class="py-3 sm:py-4 px-4 sm:px-6 text-center">
                        <div class="flex items-center justify-center gap-1 sm:gap-2">
                            <a href="${editUrl}" class="p-1.5 sm:p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors" title="Edit Data">
                                <i class="ph ph-pencil-simple text-base sm:text-lg"></i>
                            </a>
                            <form action="${deleteUrl}" method="POST" onsubmit="return confirm('Apakah Anda yakin ingin menghapus data ini?');">
                                <button type="submit" class="p-1.5 sm:p-2 text-red-500 hover:bg-red-50 rounded-lg transition-colors" title="Hapus Data">
                                    <i class="ph ph-trash text-base sm:text-lg"></i>
                                </button>
                            </form>
                        </div>
                    </td>
                `;
                
                historyTableBody.appendChild(tr);
            });
        }
        
        function updateExportUrl() {
            var exportBtn = document.getElementById('export-btn');
            if (exportBtn) {
                var exportUrl = '/export/excel?kelurahan=' + encodeURIComponent(currentKelurahan);
                if (currentSearch) {
                    exportUrl += '&search=' + encodeURIComponent(currentSearch);
                }
                exportBtn.href = exportUrl;
            }
        }

        // Setup event listener untuk tombol filter
        filterButtons.forEach(function(btn) {
            btn.addEventListener('click', function() {
                // Hapus class active dari semua tombol
                filterButtons.forEach(b => {
                    b.classList.remove('active', 'bg-blue-600', 'text-white');
                    b.classList.add('bg-gray-100', 'text-gray-700');
                });
                
                // Tambahkan class active ke tombol yang diklik
                this.classList.remove('bg-gray-100', 'text-gray-700');
                this.classList.add('active', 'bg-blue-600', 'text-white');
                
                currentKelurahan = this.getAttribute('data-filter');
                fetchHistory(currentKelurahan, currentSearch);
                updateExportUrl();
            });
        });

        // Setup Search functionality with debounce
        var searchInput = document.getElementById('searchInput');
        var clearSearchBtn = document.getElementById('clearSearchBtn');
        var searchTimeout = null;

        if (searchInput && clearSearchBtn) {
            searchInput.addEventListener('input', function(e) {
                currentSearch = e.target.value;
                
                if (currentSearch.length > 0) {
                    clearSearchBtn.classList.remove('hidden');
                } else {
                    clearSearchBtn.classList.add('hidden');
                }

                clearTimeout(searchTimeout);
                searchTimeout = setTimeout(function() {
                    fetchHistory(currentKelurahan, currentSearch);
                    updateExportUrl();
                }, 300);
            });

            clearSearchBtn.addEventListener('click', function() {
                searchInput.value = '';
                currentSearch = '';
                clearSearchBtn.classList.add('hidden');
                fetchHistory(currentKelurahan, currentSearch);
                updateExportUrl();
            });

            // Set initial state
            var urlParams = new URLSearchParams(window.location.search);
            var initialSearch = urlParams.get('search') || '';
            if (initialSearch) {
                currentSearch = initialSearch;
                searchInput.value = currentSearch;
                clearSearchBtn.classList.remove('hidden');
            }
        }
        
        // Initial fetch
        fetchHistory(currentKelurahan, currentSearch);
        updateExportUrl();
    }
});

// ==================================================================
//  6. VALIDASI NIK & NO. KK DAN PERILAKU ENTER
// ==================================================================
function validateNik(value) {
    return value.length === 16 && /^\d+$/.test(value);
}

function setupNikKkValidation() {
    var nikInput = document.getElementById('nikInput');
    var kkInput = document.getElementById('kkInput');
    var namaInput = document.getElementById('namaInput');

    if (nikInput && kkInput) {
        function handleInput(e) {
            // Hapus karakter non-digit
            var val = e.target.value.replace(/\D/g, '');
            e.target.value = val;

            if (val.length === 16) {
                e.target.classList.remove('border-red-500', 'focus:ring-red-500', 'focus:border-red-500');
                e.target.classList.add('border-green-500', 'focus:ring-green-500', 'focus:border-green-500');
            } else if (val.length > 0) {
                e.target.classList.remove('border-green-500', 'focus:ring-green-500', 'focus:border-green-500');
                e.target.classList.add('border-red-500', 'focus:ring-red-500', 'focus:border-red-500');
            } else {
                e.target.classList.remove('border-red-500', 'border-green-500', 'focus:ring-red-500', 'focus:ring-green-500', 'focus:border-red-500', 'focus:border-green-500');
            }
        }

        nikInput.addEventListener('input', handleInput);
        kkInput.addEventListener('input', handleInput);

        nikInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault(); // Cegah submit form
                kkInput.focus(); // Pindah fokus ke input KK
            }
        });

        kkInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault(); // Cegah submit form
                if (namaInput) namaInput.focus(); // Pindah fokus ke input Nama
            }
        });

        // Cegah form disubmit jika tidak valid
        var form = nikInput.closest('form');
        if (form) {
            form.addEventListener('submit', function(e) {
                if (!validateNik(nikInput.value)) {
                    e.preventDefault();
                    alert('NIK harus 16 digit angka.');
                    nikInput.focus();
                    return;
                }
                if (!validateNik(kkInput.value)) {
                    e.preventDefault();
                    alert('No. KK harus 16 digit angka.');
                    kkInput.focus();
                    return;
                }
            });
        }
    }
}

// Inisialisasi setelah DOM dimuat
document.addEventListener('DOMContentLoaded', setupNikKkValidation);

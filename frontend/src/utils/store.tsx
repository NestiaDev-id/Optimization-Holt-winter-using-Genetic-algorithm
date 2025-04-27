import dotenv from "dotenv"; // Menggunakan 'dotenv' dengan benar
dotenv.config(); // Memuat variabel lingkungan dari file .env

// Pastikan variabel 'URL' dideklarasikan dengan 'const' atau 'let'

async function getData(): Promise<any> {
  // Tipe Promise diatur untuk tipe 'any'
  try {
    const URL = process.env.URL_BACKEND || ""; // Mengambil URL dari variabel lingkungan
    const response = await fetch(`${URL}/api/`); // Memanggil fetch dengan url
    if (!response.ok) {
      // Jika respons gagal (status bukan 200-299), lemparkan error
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    // Mengembalikan data JSON
    return await response.json();
  } catch (error) {
    // Menangani error dan mencetaknya
    console.error("Error fetching data:", error);
    throw error;
  }
}

export default getData; // Menyediakan fungsi ini untuk digunakan di tempat lain

async function sendData(
  generation: string,
  kromosom: string,
  probability: string
): Promise<any> {
  const URL = process.env.URL_BACKEND || ""; // Mengambil URL dari variabel lingkungan
  try {
    const response = await fetch(`${URL}/api/predict`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        generation: generation,
        kromosom: kromosom,
        probability: probability,
      }),
    });
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error("Error sending data:", error);
    throw error;
  }
}

export { getData, sendData }; // Mengekspor fungsi untuk digunakan di tempat lain

const API_BASE_URL = "http://127.0.0.1:8000";

// Register User
export async function registerUser(name, email, password) {
  const response = await fetch(`${API_BASE_URL}/users/register`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      name: name,
      email: email,
      password: password,
    }),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Registration failed");
  }

  return data;
}


// Login User
export async function loginUser(email, password) {
  const response = await fetch(`${API_BASE_URL}/users/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      email: email,
      password: password,
    }),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Login failed");
  }

  return data;
}


// Disease Prediction
export async function predictDisease(userId, imageFile) {
  const formData = new FormData();

  formData.append("user_id", userId);
  formData.append("file", imageFile);

  const response = await fetch(
    `${API_BASE_URL}/disease/predict`,
    {
      method: "POST",
      body: formData,
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Disease prediction failed");
  }

  return data;
}
// Crop Recommendation + Market Analysis
export async function recommendCrop(userId, cropData) {
  const response = await fetch(
    `${API_BASE_URL}/crop/recommend-with-market`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        user_id: userId,
        ...cropData,
      }),
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || "Crop recommendation failed"
    );
  }

  return data;
}
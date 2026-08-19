const API = "";
let latest = null;

const $ = id => document.getElementById(id);

async function checkAPI() {
  try {
    const r = await fetch(`${API}/api/health`);
    if (!r.ok) throw new Error();
    $("apiStatus").textContent = "● API online";
    $("apiStatus").className = "online";
  } catch {
    $("apiStatus").textContent = "● API offline";
    $("apiStatus").className = "offline";
  }
}

function showError(msg) {
  $("error").textContent = msg;
  $("error").classList.remove("hidden");
}

async function gather() {
  const target = $("target").value.trim();
  if (!target) return showError("Enter a target first.");

  $("error").classList.add("hidden");
  $("results").classList.add("hidden");
  $("loading").classList.remove("hidden");
  $("scan").disabled = true;
  $("scan").textContent = "Gathering...";

  try {
    const r = await fetch(`${API}/api/recon`, {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({target})
    });

    const data = await r.json();
    if (!r.ok) throw new Error(data.error || "Backend returned an error.");

    latest = data;
    render(data);
  } catch (e) {
    showError(
      `Could not gather information. ${e.message} ` +
      `Make sure the Flask backend is running on port 5000.`
    );
  } finally {
    $("loading").classList.add("hidden");
    $("scan").disabled = false;
    $("scan").textContent = "Gather Information";
  }
}

function render(data) {
  const records = data.dns?.records || {};
  const dnsCount = Object.values(records).reduce((n, a) => n + a.length, 0);

  $("targetName").textContent = data.target;
  $("ipCount").textContent = (data.dns?.resolved_ips || []).length;
  $("dnsCount").textContent = dnsCount;
  $("httpStatus").textContent = data.http?.status_code ?? "—";
  $("rdap").textContent = data.rdap?.available ? "Available" : "Unavailable";

  $("dns").textContent = JSON.stringify(data.dns, null, 2);
  $("http").textContent = JSON.stringify(data.http, null, 2);
  $("rdapData").textContent = JSON.stringify(data.rdap, null, 2);

  $("results").classList.remove("hidden");
  $("results").scrollIntoView({behavior:"smooth"});
}

$("scan").addEventListener("click", gather);
$("target").addEventListener("keydown", e => { if (e.key === "Enter") gather(); });
$("copy").addEventListener("click", async () => {
  if (!latest) return;
  await navigator.clipboard.writeText(JSON.stringify(latest, null, 2));
  $("copy").textContent = "Copied!";
  setTimeout(() => $("copy").textContent = "Copy JSON", 1200);
});

checkAPI();

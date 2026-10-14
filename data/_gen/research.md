<ul class="research-intro">
<li>Study physics in solid-state materials: how defects & quasiparticles affect their electrical and optical properties.</li>
<li>Analyze defect states and local structure with <span class="rs-tech">transient spectroscopy (PICTS/DLTS)</span> and <span class="rs-tech">tip-enhanced nanospectroscopy</span>.</li>
<li>Develop and apply <span class="rs-method">interpretable machine learning</span> to extract physically meaningful information from experimental data.</li>
</ul>

::: {.research-theme}

## 1. Defect Physics in Solid-State Materials

<p class="rs-question">How do defects and quasiparticles shape the electrical and optical properties of solid-state materials?</p>

<div class="rs-figures">
<figure class="rs-fig" id="fig-picts_dos">
<button type="button" class="rs-zoom" aria-label="Enlarge figure"><img src="assets/research/picts_dos.webp" alt="Defect density versus activation energy in a-IGZO at gate biases of 0, -5 and -10 V and after removing the bias." loading="lazy" style="width: 131px"></button>
<figcaption><span class="rs-fig-num">Fig. 1.</span> Defect density versus activation energy in a-IGZO before and after negative gate bias. <span class="rs-fig-src"><a href="publications.html#pub-1">Sci. Rep. 2023</a></span></figcaption>
</figure>
<figure class="rs-fig" id="fig-defect_band">
<button type="button" class="rs-zoom" aria-label="Enlarge figure"><img src="assets/research/defect_band.webp" alt="Band alignment of ITZO and IGZO, defect densities versus ITZO thickness, and band diagrams of trapping under bias stress." loading="lazy" style="width: 344px"></button>
<figcaption><span class="rs-fig-num">Fig. 2.</span> Defect states and bias-stress threshold shifts in ITZO/IGZO thin-film transistors. <span class="rs-fig-src"><a href="publications.html#pub-8">Surf. Interfaces 2025</a></span></figcaption>
</figure>
</div>


<div class="rs-narrative">
<p class="rs-p">Defects set the limits of many semiconductor devices: they trap carriers, pin the Fermi level, and shift device characteristics under electrical stress. This line of work began with <span class="rs-mat">amorphous oxide semiconductors</span>, where defect states were resolved over a wide energy range below the conduction band (<a class="rs-figref" href="#fig-picts_dos">Fig. 1</a>; <a href="publications.html#pub-1">Sci. Rep. 2023</a>). In ITZO/IGZO bilayer thin-film transistors, defect states above and below the Fermi level track the threshold-voltage shifts under positive and negative bias stress, which explains how the bilayer combines high mobility with stability (<a class="rs-figref" href="#fig-defect_band">Fig. 2</a>; <a href="publications.html#pub-8">Surf. Interfaces 2025</a>). Related studies examined double-gate operation and hydrogen-related defects under bias-temperature stress (<a href="publications.html#pub-2">IEEE Trans. Electron Devices 2024</a>; <a href="publications.html#pub-3">ACS Appl. Electron. Mater. 2024</a>).</p>
<p class="rs-p">I am now carrying these questions into <span class="rs-mat">two-dimensional semiconductors</span>, where defects can change the carrier type of an atomically thin channel. Ongoing work uses defect engineering to obtain n- and p-type behavior for complementary devices, and examines how excitons, the quasiparticles that dominate the optical response of 2D semiconductors, are modulated by coupling to <span class="rs-mat">plasmonic nanostructures</span>.</p>
</div>

:::

::: {.research-theme}

## 2. Defect and Nanoscale Spectroscopy

<p class="rs-question">How can defect states and local structure be measured, from devices to the nanoscale?</p>

<div class="rs-figures">
<figure class="rs-fig" id="fig-picts_principle">
<button type="button" class="rs-zoom" aria-label="Enlarge figure"><img src="assets/research/picts_principle.webp" alt="Schematic of PICTS on an IGZO thin-film transistor, with the light pulse and the resulting current transient." loading="lazy" style="width: 205px"></button>
<figcaption><span class="rs-fig-num">Fig. 3.</span> Principle of photo-induced current transient spectroscopy (PICTS). <span class="rs-fig-src"><a href="publications.html#pub-1">Sci. Rep. 2023</a></span></figcaption>
</figure>
</div>


<div class="rs-narrative">
<p class="rs-p">Answering these questions requires measuring defects directly. <span class="rs-tech">Photo-induced current transient spectroscopy (PICTS)</span> does this electrically: a light pulse fills trap states, and the current transient that follows as carriers are released yields defect energies and densities (<a class="rs-figref" href="#fig-picts_principle">Fig. 3</a>; <a href="publications.html#pub-1">Sci. Rep. 2023</a>). Together with <span class="rs-tech">deep-level transient spectroscopy (DLTS)</span>, I am extending this approach to 2D semiconductors.</p>
<p class="rs-p">Transient methods average over a whole device, so I complement them with <span class="rs-tech">tip-enhanced Raman spectroscopy (TERS)</span>, which maps defects and strain below the optical diffraction limit. Interpreting such nanoscale signals quantitatively depends on the near field at the tip apex, which I model with finite-difference time-domain (FDTD) simulations (<a href="publications.html#pub-9">Mater. Des. 2026</a>).</p>
</div>

:::

::: {.research-theme}

## 3. Interpretable AI for Science

<p class="rs-question">How can machine learning extract physically meaningful information from experimental data?</p>

<div class="rs-figures">
<figure class="rs-fig" id="fig-precision_fdtd">
<button type="button" class="rs-zoom" aria-label="Enlarge figure"><img src="assets/research/precision_fdtd.webp" alt="FP64 versus FP32 results for water geometry optimization and for FDTD transmittance spectra and second-harmonic response of a Kerr medium." loading="lazy" style="width: 469px"></button>
<figcaption><span class="rs-fig-num">Fig. 4.</span> Single (FP32) versus double (FP64) precision in DFT and nonlinear FDTD simulations. <span class="rs-fig-src"><a href="publications.html#pub-10">ICML 2026</a></span></figcaption>
</figure>
</div>


<div class="rs-narrative">
<p class="rs-p">Spectra and transients often contain more physical information than conventional peak fitting extracts. I use <span class="rs-method">machine learning</span> to recover it, with the requirement that the result remain physically interpretable: relating Raman spectral features to electrical properties, and reducing noise in experimental spectra while preserving peak positions and widths. Machine learning also meets devices directly, in simulations of analog in-memory learning based on the measured synaptic characteristics of ferroelectric InSe devices.</p>
<p class="rs-p">Reliability is a central concern. Even numerical precision can change a scientific conclusion: in DFT and nonlinear FDTD simulations, single precision produces unphysical geometries and misses weak harmonic signals that double precision resolves (<a class="rs-figref" href="#fig-precision_fdtd">Fig. 4</a>; <a href="publications.html#pub-10">ICML 2026</a>). An invited review in preparation examines when a machine-learning explanation of a spectrum can count as physical evidence.</p>
</div>

:::


<dialog class="rs-dialog" aria-label="Enlarged figure">
<form method="dialog"><button class="rs-dialog-close" aria-label="Close">&times;</button></form>
<img alt="">
<p class="rs-dialog-cap"></p>
</dialog>
<script>
(() => {
  const dialog = document.querySelector(".rs-dialog");
  if (!dialog || !dialog.showModal) return;
  document.documentElement.classList.add("rs-js");
  const img = dialog.querySelector("img"), cap = dialog.querySelector(".rs-dialog-cap");
  document.querySelectorAll(".rs-zoom").forEach(button => button.addEventListener("click", () => {
    const thumb = button.querySelector("img");
    img.src = thumb.currentSrc || thumb.src;
    img.alt = thumb.alt;
    cap.innerHTML = button.closest("figure").querySelector("figcaption").innerHTML;
    dialog.showModal();
  }));
  dialog.addEventListener("click", event => { if (event.target === dialog) dialog.close(); });
})();
</script>

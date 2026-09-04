    def test_kaplan_yorke_edge_cases(self):
        """Validates D_KY formula against specific synthetic spectrums."""
        # 1. Fully dissipative (all negative) -> D = 0
        spec1 = np.array([-1.0, -2.0, -3.0])
        self.assertEqual(LyapunovAnalyzer.kaplan_yorke_dimension(spec1), 0.0)
        
        # 2. Fully divergent (all positive) -> D = dimension length
        spec2 = np.array([1.0, 2.0, 3.0])
        self.assertEqual(LyapunovAnalyzer.kaplan_yorke_dimension(spec2), 3.0)
        
        # 3. Standard fractional fractal dimension
        # sum(L1) = 0.5 (j=1). L2 = -2.0. D_KY = 1 + (0.5 / |-2.0|) = 1.25
        spec3 = np.array([0.5, -2.0, -3.0])
        self.assertAlmostEqual(LyapunovAnalyzer.kaplan_yorke_dimension(spec3), 1.25)

    def test_full_spectrum_orthogonality(self):
        """Validates that the tangent matrix V remains perfectly orthogonal (E_Q ~ 0) via QR."""
        def stable_2d(t, state):
            return [-0.5 * state[0], -0.2 * state[1]]
            
        analyzer = LyapunovAnalyzer(stable_2d, dimension=2)
        res = analyzer.calculate_full_spectrum(y0=np.array([1.0, 1.0]), t_max=10.0, tau_r=1.0)
        
        # Check maximum orthogonality error
        max_error = np.max(res['orthogonality_errors'])
        self.assertLess(max_error, 1e-10)
        
        # Expect spectrum to match the stable eigenvalues: -0.2 and -0.5 (sorted)
        self.assertAlmostEqual(res['final_spectrum'][0], -0.2, places=2)
        self.assertAlmostEqual(res['final_spectrum'][1], -0.5, places=2)

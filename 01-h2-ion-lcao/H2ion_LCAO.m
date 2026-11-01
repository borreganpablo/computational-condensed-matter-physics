% =========================================================================
%  H2+ molecular ion: variational LCAO approximation (minimal 1s basis)
%  Author: Pablo Borregan Jimeno
%
%  Builds the 2x2 Hamiltonian and overlap matrices from the analytic
%  1s integrals, solves the generalized eigenvalue problem H c = E S c
%  for each internuclear distance R, and finds the equilibrium bond length.
%  Atomic units throughout (energies in Hartree, distances in bohr).
% =========================================================================

clear; clc; close all;

R_vec = linspace(0.5, 15, 200);          % internuclear distances (bohr)
E_el  = zeros(size(R_vec));              % electronic ground-state energy

for k = 1:length(R_vec)
    R = R_vec(k);

    % Analytic matrix elements for two hydrogen 1s orbitals
    S12 = exp(-R) * (1 + R + R^2/3);              % overlap integral
    J   = (1/R) * (1 - (1 + R)*exp(-2*R));        % Coulomb integral
    K   = (1 + R) * exp(-R);                      % exchange (resonance) integral

    H11 = -0.5 - J;
    H12 = -0.5*S12 - K;

    S = [1,   S12;  S12, 1  ];
    H = [H11, H12;  H12, H11];

    % Generalized eigenvalue problem H c = E S c
    E_el(k) = min(eig(H, S));
end

% Total energy = electronic energy + nuclear repulsion 1/R
E_tot = E_el + 1 ./ R_vec;

% Equilibrium distance and minimum energy
[E_min, idx] = min(E_tot);
Re = R_vec(idx);
De = -0.5 - E_min;                                % dissociation energy

fprintf('--- H2+ (minimal 1s basis) ---\n');
fprintf('Equilibrium distance  Re = %.3f bohr\n', Re);
fprintf('Minimum total energy  E  = %.4f Hartree\n', E_min);
fprintf('Dissociation energy   De = %.4f Hartree (%.2f eV)\n', De, De*27.2114);

% Plot
figure('Position', [100, 100, 800, 550]);
hold on; grid on; box on;
plot(R_vec, E_el,  '--b', 'LineWidth', 1.5, 'DisplayName', 'E_{el}');
plot(R_vec, E_tot, '-b',  'LineWidth', 2,   'DisplayName', 'E_{tot} = E_{el} + 1/R');
plot(Re, E_min, 'ok', 'MarkerSize', 8, 'MarkerFaceColor', 'y', ...
     'DisplayName', sprintf('Minimum (R_e = %.2f bohr, E = %.3f Ha)', Re, E_min));
yline(-0.5, ':k', 'DisplayName', 'H + H^+ limit');
xlabel('Internuclear distance R (bohr)');
ylabel('Energy (Hartree)');
title('H_2^+ potential energy curve (LCAO, 1s basis)');
xlim([0, 10]); ylim([-1.2, 0.2]);
legend('Location', 'southeast');
hold off;
saveas(gcf, 'h2_ion_energy.png');

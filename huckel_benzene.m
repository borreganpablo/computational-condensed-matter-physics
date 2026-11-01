% =========================================================================
%  Hückel model of the pi-electron system of benzene
%  Author: Pablo Borregan Jimeno
%
%  Builds the 6x6 Hückel Hamiltonian of a ring of six carbon atoms
%  (periodic boundary conditions) and solves it symbolically for the
%  energy eigenvalues and molecular orbitals (eigenvectors).
%  Requires the MATLAB Symbolic Math Toolbox.
% =========================================================================

clear; clc;

% Coulomb integral alpha and resonance integral beta (beta < 0 physically)
syms alpha beta_sym real

% Hückel Hamiltonian: alpha on the diagonal, beta between neighbours.
% The corner elements close the ring (atom 6 bonded to atom 1).
H = [alpha,    beta_sym, 0,        0,        0,        beta_sym;
     beta_sym, alpha,    beta_sym, 0,        0,        0;
     0,        beta_sym, alpha,    beta_sym, 0,        0;
     0,        0,        beta_sym, alpha,    beta_sym, 0;
     0,        0,        0,        beta_sym, alpha,    beta_sym;
     beta_sym, 0,        0,        0,        beta_sym, alpha];

% Eigenvalues (diagonal of D) and eigenvectors (columns of V)
[V, D] = eig(H);
V = simplify(V);
D = simplify(D);

fprintf('--- Energy eigenvalues ---\n');
disp(diag(D));
fprintf('--- Molecular orbitals (columns) ---\n');
disp(V);

% Note: MATLAB sorts symbolic eigenvalues algebraically and does not know
% that beta < 0. Physically the ordering from lowest to highest energy is
%   alpha + 2*beta < alpha + beta (x2) < alpha - beta (x2) < alpha - 2*beta
% With 6 pi electrons the three bonding orbitals are filled, giving a total
% pi energy of 6*alpha + 8*beta: the delocalisation (aromatic) energy is
% 2*beta lower than three isolated C=C bonds (6*alpha + 6*beta).
